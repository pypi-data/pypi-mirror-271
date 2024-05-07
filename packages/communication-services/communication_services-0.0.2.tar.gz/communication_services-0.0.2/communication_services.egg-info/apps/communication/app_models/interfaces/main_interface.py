from django.apps import apps
from django.db.models import Model


#EXP: db_add(YourModel, field1='value1', field2='value2')
def db_add(model_class, **kwargs):
    """
    Add a new instance to the specified model.

    :param model_class: The model class.
    :param kwargs: Keyword arguments containing field names and their values.
    :return: The created instance if successful, None otherwise.
    """
    if issubclass(model_class, Model):
        instance = model_class.objects.create(**kwargs)
        return instance
    return None


#EXP: db_get_by_id(YourModel, instance_id=1)
def db_get_by_id(model_class, instance_id):
    """
    Retrieve an instance from the specified model by ID.

    :param model_class: The model class.
    :param instance_id: The ID of the instance.
    :return: The instance if found, None otherwise.
    """
    if issubclass(model_class, Model):
        try:
            instance = model_class.objects.get(id=instance_id)
            return instance
        except model_class.DoesNotExist:
            pass
    return None


#EXP: db_update(YourModel, instance_id=1, field1='new_value')

def db_update(model_class, instance_id, **kwargs):
    """
    Update an instance in the specified model.

    :param model_class: The model class.
    :param instance_id: The ID of the instance to be updated.
    :param kwargs: Keyword arguments containing field names and their updated values.
    :return: True if the update was successful, False otherwise.
    """
    if issubclass(model_class, Model):
        try:
            instance = model_class.objects.get(id=instance_id)
            for field, value in kwargs.items():
                setattr(instance, field, value)
            instance.save()
            return True
        except model_class.DoesNotExist:
            pass
    return False

#EXP: db_delete(YourModel, instance_id=1)
def db_delete(model_class, instance_id):
    """
    Delete an instance from the specified model by ID.

    :param model_class: The model class.
    :param instance_id: The ID of the instance to be deleted.
    :return: True if the deletion was successful, False otherwise.
    """
    if issubclass(model_class, Model):
        try:
            instance = model_class.objects.get(id=instance_id)
            instance.delete()
            return True
        except model_class.DoesNotExist:
            pass
    return False
#EXP: db_get_by_filter(YourModel, field1='value1', field2='value2')
def db_get_by_filter(model_class, **kwargs):
    """
    Filter instances from the specified model based on the provided filter criteria.

    :param model_class: The model class.
    :param kwargs: Keyword arguments containing filter criteria (field names and values).
    :return: QuerySet containing filtered instances.
    """
    if issubclass(model_class, Model):
        queryset = model_class.objects.filter(**kwargs)
        return queryset
    return None