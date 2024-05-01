import logging
import sys
import uuid
from datetime import timedelta, datetime as py_datetime
from django.core.cache import cache
from cached_property import cached_property
from django.apps import apps
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.db import models
from django.utils.crypto import salted_hmac
from graphql import ResolveInfo
import core
#from core.datetimes.ad_datetime import datetime as py_datetime
from django.conf import settings

from ..utils import filter_validity
from .base import *
from .versioned_model import *

logger = logging.getLogger(__name__)

from .user import User, _query_export_path, _get_default_expire_date



class ExportableQueryModel(models.Model):
    name = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    content = models.FileField(upload_to=_query_export_path)

    user = models.ForeignKey(
        User, db_column="User", related_name='data_exports',
        on_delete=models.deletion.DO_NOTHING, null=False)

    sql_query = models.TextField()
    create_date = DateTimeField(db_column='DateCreated', default=py_datetime.now)
    expire_date = DateTimeField(db_column='DateExpiring', default=_get_default_expire_date)
    is_deleted = models.BooleanField(default=False)

    @staticmethod
    def create_csv_export(qs, values, user, column_names=None,
                          patches=None):
        if patches is None:
            patches = []
        sql = qs.query.sql_with_params()
        content = DataFrame.from_records(qs.values_list(*values))
        content.columns = values
        for patch in patches:
            content = patch(content)

        content.columns = [column_names.get(column) or column for column in content.columns]
        filename = F"{uuid.uuid4()}.csv"
        content = ContentFile(content.to_csv(), filename)
        export = ExportableQueryModel(
            name=filename,
            model=qs.model.__name__,
            content=content,
            user=user,
            sql_query=sql,
        )
        export.save()
        return export
    


class MutationLog(UUIDModel, ExtendableModel):
    """
    Maintains a log of every mutation requested along with its status. It is used to reply
    immediately to the client and have longer processing in the various backend modules.
    The ID of this table will be used for reference.
    """
    RECEIVED = 0
    ERROR = 1
    SUCCESS = 2
    STATUS_CHOICES = (
        (RECEIVED, "Received"),
        (ERROR, "Error"),
        (SUCCESS, "Success"),
    )

    json_content = models.TextField()
    user = models.ForeignKey(User, on_delete=DO_NOTHING, blank=True, null=True)
    request_date_time = models.DateTimeField(auto_now_add=True)
    client_mutation_id = models.CharField(
        max_length=255, blank=True, null=True)
    client_mutation_label = models.CharField(
        max_length=255, blank=True, null=True)
    client_mutation_details = models.TextField(blank=True, null=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=RECEIVED)
    error = models.TextField(blank=True, null=True)
    autogenerated_code = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = "core_Mutation_Log"

    def mark_as_successful(self):
        """
        Do not alter the mutation_log and then save it as it might override changes from another process. This
        method will only set the mutation_log as successful if it is in RECEIVED status.
        :return True if the status was updated, False if it was in ERROR or already in SUCCESS status
        """
        affected_rows = MutationLog.objects.filter(id=self.id) \
            .filter(status=MutationLog.RECEIVED).update(status=MutationLog.SUCCESS)
        self.refresh_from_db()
        return affected_rows > 0

    def mark_as_failed(self, error):
        """
        Do not alter the mutation_log and then save it as it might override changes from another process.
        This method will force the status to ERROR and set its error accordingly.
        """
        MutationLog.objects.filter(id=self.id) \
            .update(status=MutationLog.ERROR, error=error)
        self.refresh_from_db()


class ObjectMutation:
    """
    This object is used for link tables between the business objects and the MutationLog like ClaimMutation.
    The object_mutated() method allows the creation of an object to update the xxxMutation easily.

    Declare the Mutation model as:
        class PaymentMutation(core_models.UUIDModel, core_models.ObjectMutation):
        payment = models.ForeignKey(Payment, models.DO_NOTHING, related_name='mutations')
        mutation = models.ForeignKey(core_models.MutationLog, models.DO_NOTHING, related_name='payments')

        class Meta:
            managed = True
            db_table = "contribution_PaymentMutation"

    Call it like:
        client_mutation_id = data.get("client_mutation_id")
        payment = update_or_create_payment(data, user)
        PaymentMutation.object_mutated(user, client_mutation_id=client_mutation_id, payment=payment)
        return None

    Note that payment=payment, the name of the parameter gives the field name of the xxxMutation object to use
    and the value is the instance itself.
    """

    @classmethod
    def object_mutated(cls, user, mutation_log_id=None, client_mutation_id=None, *args, **kwargs):
        # This method should fail silently to not disrupt the actual mutation
        # noinspection PyBroadException
        try:
            args_models = {k + "_id": v.id for k, v in kwargs.items() if isinstance(v, models.Model)}
            if len(args_models) == 0 or len(args_models) > 1:
                logger.error("Trying to update ObjectMutationLink with several models in params: %s",
                             ", ".join(args_models.keys()))
                return
            if mutation_log_id:
                cls.objects.get_or_create(mutation_id=mutation_log_id, **args_models)
            elif client_mutation_id:
                mutations = MutationLog.objects \
                    .filter(client_mutation_id=client_mutation_id) \
                    .filter(user=user) \
                    .values_list("id", flat=True) \
                    .order_by("-request_date_time")[:2]  # Only ask for 2 for the warning, we'll only use 1
                if len(mutations) == 2:
                    # Warning because if done too often, this would cause performance issues in this query
                    logger.warning("Two or more mutations found for id %s, using the most recent one",
                                   client_mutation_id)
                if len(mutations) == 0:
                    logger.debug("No mutation found for client_mutation_id %s, ignoring", client_mutation_id)
                    return
                cls.objects.get_or_create(mutation_id=mutations[0], **args_models)
            else:
                logger.warning(
                    "Trying to update a %s without either mutation id or client_mutation_id, ignoring", cls.__name__)
        except Exception as exc:
            # The mutation shouldn't fail because we couldn't store the UUID
            logger.error("Error updating the %s object", cls.__name__, exc_info=True)

