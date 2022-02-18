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

    # def save(self, *args, **kwargs):
    #     self.rdep_name = self.rdep_name.upper()
    #     self.rdep_full_name = self.rdep_full_name.upper()
    #     super().save(*args, **kwargs)

    class Meta:
        db_table = 'RFT_STATION'
        verbose_name = 'Станция'
        verbose_name_plural = 'Станции'
        ordering = ['st_code']
