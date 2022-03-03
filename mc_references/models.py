from django.db import models


class RftFirmCode(models.Model):
    """Справочник фирм."""
    FRCT_IDE = (
        (1, 'Экспедитор'),
        (2, 'ТГНЛ'),
        (3, 'Арендатор'),
        (4, 'Собственник'),
    )

    frc_code = models.CharField(
        db_index=True,
        max_length=10,
        verbose_name='Код ГВЦ')
    frct_ide = models.SmallIntegerField(
        choices=FRCT_IDE,
        verbose_name='Тип юр. лица')
    okpo = models.CharField(
        db_index=True,
        max_length=10,
        verbose_name='ОКПО')
    frm_short_name = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name='Краткое наименование фирмы')
    frm_name = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name='Наименоване фирмы')
    update_date = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='Дата обновления')

    def __str__(self) -> str:
        return f'#{self.frc_code} ({self.okpo}) {self.frm_short_name}'

    class Meta:
        db_table = 'RFT_FIRM_CODE'
        verbose_name = 'Фирма'
        verbose_name_plural = 'Фирмы'
        ordering = ['frc_code']


class RftCountry(models.Model):
    """Справочник стран."""
    cnt_ide = models.CharField(
        primary_key=True,
        max_length=3,
        verbose_name='Код страны'
    )
    cnt_name = models.CharField(
        max_length=100,
        verbose_name='Наименование страны'
    )
    update_date = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='Дата обновления')

    def __str__(self) -> str:
        return f'#{self.cnt_ide} - {self.cnt_name}'

    def save(self, *args, **kwargs):
        self.cnt_name = self.cnt_name.capitalize()
        super().save(*args, **kwargs)

    @staticmethod
    def get_by_id(pk_id: str):
        if pk_id:
            return RftCountry.objects.get(pk=str(pk_id).rjust(3, "0"))

    class Meta:
        db_table = 'RFT_COUNTRY'
        verbose_name = 'Страна'
        verbose_name_plural = 'Страны'
        ordering = ['cnt_ide']


class RftOperation(models.Model):
    """Справочник операций."""
    TRANSP_TYPE = (
        (0, 'Вагон'),
        (1, 'Контейнер'),
    )

    o_code = models.CharField(
        db_index=True,
        max_length=2,
        verbose_name='Код операции'
    )
    o_name = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name='Наименование'
    )
    o_description = models.CharField(
        max_length=200,
        verbose_name='Полное наименование'
    )
    transp_type = models.SmallIntegerField(
        choices=TRANSP_TYPE,
        verbose_name='Тип транспортного средства')
    update_date = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='Дата обновления')

    def __str__(self) -> str:
        return f'#{self.o_code} - {self.o_name}'

    class Meta:
        db_table = 'RFT_OPERATION'
        verbose_name = 'Операция'
        verbose_name_plural = 'Операции'
        ordering = ['o_code']


class RftCargoEtsng(models.Model):
    """Справочник грузов ЕТСНГ."""
    crg_code = models.IntegerField(
        primary_key=True,
        verbose_name='Код грузы'
    )
    crg_name = models.CharField(
        max_length=100,
        verbose_name='Наименование'
    )
    update_date = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='Дата обновления')

    def __str__(self) -> str:
        return f'#{self.crg_code} - {self.crg_name}'

    def save(self, *args, **kwargs):
        self.crg_name = self.crg_name.capitalize()
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'RFT_CARGO_ETSNG'
        verbose_name = 'Груз'
        verbose_name_plural = 'Грузы'
        ordering = ['crg_code']


class RftRailway(models.Model):
    """Справочник дорог."""
    rlw_code = models.CharField(
        primary_key=True,
        max_length=2,
        verbose_name='Код дороги'
    )
    rlw_name = models.CharField(
        max_length=3,
        verbose_name='Краткое наименование дороги'
    )
    rlw_full_name = models.CharField(
        max_length=100,
        verbose_name='Наименование дороги'
    )
    cntr_ide = models.ForeignKey(
        RftCountry,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        verbose_name='Страна'
    )
    update_date = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='Дата обновления')

    def __str__(self) -> str:
        return f'#{self.rlw_code} ({self.rlw_name}) - {self.rlw_full_name}'

    def save(self, *args, **kwargs):
        self.rlw_full_name = self.rlw_full_name.upper()
        super().save(*args, **kwargs)

    @staticmethod
    def get_by_id(pk_id: str):
        if pk_id:
            return RftRailway.objects.get(pk=pk_id.rjust(2, "0"))

    class Meta:
        db_table = 'RFT_RAILWAY'
        verbose_name = 'Дорога'
        verbose_name_plural = 'Дороги'
        ordering = ['rlw_name']


class RftRlwDep(models.Model):
    """Справочник отделений."""
    rdep_ide = models.IntegerField(
        primary_key=True,
        verbose_name='Идентификатор отделения'
    )
    rdep_code = models.CharField(
        max_length=2,
        verbose_name='Код отделения'
    )
    rdep_name = models.CharField(
        max_length=100,
        verbose_name='Краткое наименование отделения'
    )
    rdep_full_name = models.CharField(
        max_length=100,
        verbose_name='Наименование отделения'
    )
    rlw_code = models.ForeignKey(
        RftRailway,
        on_delete=models.PROTECT,
        verbose_name='Дорога'
    )
    update_date = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='Дата обновления')

    def __str__(self) -> str:
        return f'#{self.rdep_ide} - {self.rdep_full_name}'

    def save(self, *args, **kwargs):
        self.rdep_name = self.rdep_name.upper()
        self.rdep_full_name = self.rdep_full_name.upper()
        super().save(*args, **kwargs)

    @staticmethod
    def get_by_id(pk_id: str):
        if pk_id:
            return RftRlwDep.objects.get(rdep_ide=int(pk_id))

    class Meta:
        db_table = 'RFT_RLW_DEP'
        verbose_name = 'Отделение'
        verbose_name_plural = 'Отделения'
        ordering = ['rdep_ide']


class RftStation(models.Model):
    """Справочник станций."""
    st_code = models.CharField(
        primary_key=True,
        max_length=5,
        verbose_name='Код станции'
    )
    st_code_6 = models.CharField(
        max_length=6,
        verbose_name='Код станции (6-символьный)'
    )
    st_full_name = models.CharField(
        max_length=100,
        verbose_name='Наименование станции'
    )
    rlw_code = models.ForeignKey(
        RftRailway,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        verbose_name='Дорога'
    )
    rdep_ide = models.ForeignKey(
        RftRlwDep,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        verbose_name='Отделение'
    )
    cntr_ide = models.ForeignKey(
        RftCountry,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        verbose_name='Страна'
    )
    update_date = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='Дата обновления')

    def __str__(self) -> str:
        return f'#{self.st_code} - {self.st_full_name}'

    class Meta:
        db_table = 'RFT_STATION'
        verbose_name = 'Станция'
        verbose_name_plural = 'Станции'
        ordering = ['st_code']


class RftDepo(models.Model):
    """Справочник депо."""
    dp_code = models.CharField(
        primary_key=True,
        max_length=4,
        verbose_name='Код депо'
    )
    dp_name = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name='Наименование депо'
    )
    dp_update_date = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='Дата обновления')

    def __str__(self) -> str:
        return f'#{self.dp_code} - {self.dp_name}'

    @staticmethod
    def get_by_id(pk_id: str):
        if pk_id:
            return RftDepo.objects.get(pk=str(pk_id).rjust(4, "0"))

    class Meta:
        db_table = 'RFT_DEPO'
        verbose_name = 'Депо'
        verbose_name_plural = 'Депо'
        ordering = ['dp_code']


class RftRwcType(models.Model):
    """Справочник родов вагонов."""
    rt_code = models.CharField(
        primary_key=True,
        max_length=2,
        verbose_name='Код рода вагона'
    )
    rt_name = models.CharField(
        max_length=100,
        verbose_name='Наименование рода вагона'
    )
    update_date = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='Дата обновления')

    def __str__(self) -> str:
        return f'#{self.rt_code} - {self.rt_name}'

    @staticmethod
    def get_by_id(pk_id: str):
        if pk_id:
            return RftRwcType.objects.get(pk=str(pk_id).rjust(2, "0"))

    class Meta:
        db_table = 'RFT_RWC_TYPE'
        verbose_name = 'Род вагона'
        verbose_name_plural = 'Роды вагонов'
        ordering = ['rt_code']


class RftRwcModel(models.Model):
    """Справочник моделей вагонов."""
    rm_code = models.CharField(
        primary_key=True,
        max_length=20,
        verbose_name='Код модели вагона'
    )
    rm_osob = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='Наименование модели вагона'
    )
    update_date = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='Дата обновления')

    def __str__(self) -> str:
        return f'#{self.rm_code} - {self.rm_osob}'

    @staticmethod
    def get_by_id(pk_id: str):
        if pk_id:
            return RftRwcModel.objects.get(pk=pk_id)

    class Meta:
        db_table = 'RFT_RWC_MODEL'
        verbose_name = 'Модель вагона'
        verbose_name_plural = 'Модели вагонов'
        ordering = ['rm_code']


class RftContType(models.Model):
    """Справочник типов контейнеров."""
    ct_code = models.CharField(
        primary_key=True,
        max_length=20,
        verbose_name='Код типа контейнера'
    )
    ct_name = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='Наименование типа контейнера'
    )
    update_date = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='Дата обновления')

    def __str__(self) -> str:
        return f'#{self.ct_code} - {self.ct_name}'

    @staticmethod
    def get_by_id(pk_id: str):
        if pk_id:
            return RftContType.objects.get(pk=pk_id)

    class Meta:
        db_table = 'RFT_CONT_TYPE'
        verbose_name = 'Тип контейнера'
        verbose_name_plural = 'Типы контейнеров'
        ordering = ['ct_code']


class RftRepairType(models.Model):
    """Справочник типов ремонтов."""
    rpt_code = models.CharField(
        primary_key=True,
        max_length=2,
        verbose_name='Код типа ремонта'
    )
    rpt_name = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='Наименование типа ремонта'
    )
    update_date = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='Дата обновления')

    def __str__(self) -> str:
        return f'#{self.rpt_code} - {self.rpt_name}'

    @staticmethod
    def get_by_id(pk_id: str):
        if pk_id:
            return RftRepairType.objects.get(pk=pk_id)

    class Meta:
        db_table = 'RFT_REPAIR_TYPE'
        verbose_name = 'Тип ремонта'
        verbose_name_plural = 'Типы ремонтов'
        ordering = ['rpt_code']


class RftRwcFault(models.Model):
    """Справочник неисправностей."""
    flt_code = models.CharField(
        primary_key=True,
        max_length=3,
        verbose_name='Код неисправности'
    )
    flt_name = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='Наименование неисправности'
    )
    update_date = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='Дата обновления')

    def __str__(self) -> str:
        return f'#{self.flt_code} - {self.flt_name}'

    @staticmethod
    def get_by_id(pk_id: str):
        if pk_id:
            return RftRwcFault.objects.get(pk=pk_id)

    class Meta:
        db_table = 'RFT_RWC_FAULT'
        verbose_name = 'Неисправность'
        verbose_name_plural = 'Неисправности'
        ordering = ['flt_code']


class RwcFaultCause(models.Model):
    """Справочник причин неисправностей."""
    cause_ide = models.CharField(
        primary_key=True,
        max_length=1,
        verbose_name='Код причины'
    )
    cause_name = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='Наименование причины'
    )

    def __str__(self) -> str:
        return f'#{self.cause_ide} - {self.cause_name}'

    @staticmethod
    def get_by_id(pk_id: str):
        if pk_id:
            return RwcFaultCause.objects.get(pk=pk_id)

    class Meta:
        db_table = 'RWC_FAULT_CAUSE'
        verbose_name = 'Причина неисправности'
        verbose_name_plural = 'Причины неисправностей'
        ordering = ['cause_ide']


class RftServiceType(models.Model):
    """Справочник типов обслуживания."""
    srvt_ide = models.CharField(
        primary_key=True,
        max_length=1,
        verbose_name='Код типа'
    )
    srvt_name = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='Наименование типа'
    )

    def __str__(self) -> str:
        return f'#{self.srvt_ide} - {self.srvt_name}'

    @staticmethod
    def get_by_id(pk_id: str):
        if pk_id:
            return RftServiceType.objects.get(pk=pk_id)

    class Meta:
        db_table = 'RFT_SERVICE_TYPE'
        verbose_name = 'Тип обслуживания'
        verbose_name_plural = 'Типы обслуживания'
        ordering = ['srvt_ide']


class RftRwcCnd(models.Model):
    """Справочник состояния вагонов."""
    cnd_code = models.CharField(
        primary_key=True,
        max_length=1,
        verbose_name='Код состояния'
    )
    cnd_name = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='Наименование состояния'
    )

    def __str__(self) -> str:
        return f'#{self.cnd_code} - {self.cnd_name}'

    @staticmethod
    def get_by_id(pk_id: str):
        if pk_id:
            return RftRwcCnd.objects.get(pk=pk_id)

    class Meta:
        db_table = 'RFT_RWC_CND'
        verbose_name = 'Состояние вагона'
        verbose_name_plural = 'Состояния вагонов'
        ordering = ['cnd_code']


class RftRwcGroup(models.Model):
    """Справочник групп вагонов."""
    rwc_group = models.IntegerField(
        primary_key=True,
        verbose_name='Код группы'
    )
    rwc_group_name = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='Наименование группы'
    )
    rwc_parent_group = models.IntegerField(
        default=0,
        verbose_name='Код род. группы'
    )
    rwc_top_group = models.IntegerField(
        default=0,
        verbose_name='Код группы верхнего уровня'
    )
    update_date = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='Дата обновления')

    def __str__(self) -> str:
        return f'#{self.rwc_group} - {self.rwc_group_name}'

    @staticmethod
    def get_by_id(pk_id: str):
        if pk_id:
            return RftRwcGroup.objects.get(pk=int(pk_id))

    class Meta:
        db_table = 'RFT_RWC_GROUP'
        verbose_name = 'Группа вагона'
        verbose_name_plural = 'Группы вагонов'
        ordering = ['rwc_group']
