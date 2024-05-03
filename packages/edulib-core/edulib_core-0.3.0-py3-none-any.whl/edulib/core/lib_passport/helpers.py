import json


def sync_m2m_field(obj, fieldname, pks):
    """Синхронизация поля `Многие ко многим' со списком идентификаторов.
    """
    rel_manager = getattr(obj, fieldname)

    # Удаляем ненужные реестры:
    need_remove = rel_manager.exclude(pk__in=pks).values_list("pk", flat=True)
    rel_manager.remove(*need_remove)

    # Добавляем новые реестры (существующие игнорируем):
    rel_manager.add(*pks)


def save_m2m_relation(obj, names_dict, context):
    """ Функция создания связи m2m по наименованию атрибутов объекта """
    for name, _ in names_dict.items():
        if hasattr(context, name) and hasattr(obj, name):
            ids_list = json.loads(getattr(context, name))
            # получаем атрибут объекта, который m2m
            sync_m2m_field(obj, name, ids_list)
