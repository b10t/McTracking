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

    class Meta:
        db_table = 'RFT_CARGO_ETSNG'
        verbose_name = 'Груз'
        verbose_name_plural = 'Грузы'
        ordering = ['crg_code']
