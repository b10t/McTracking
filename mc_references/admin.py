from django.contrib import admin

from .models import (RftCargoEtsng, RftCountry, RftFirmCode, RftOperation,
                     RftRailway, RftRlwDep, RftStation)


@admin.register(RftFirmCode)
class RftFirmCodeAdmin(admin.ModelAdmin):
    list_display = ('frc_code', 'okpo', 'frct_ide',
                    'frm_short_name', 'update_date', )
    list_display_links = ('frc_code', 'okpo', 'frm_short_name', )
    search_fields = ('frc_code', 'okpo', 'frm_short_name', 'frm_name')


@admin.register(RftCountry)
class RftCountryAdmin(admin.ModelAdmin):
    list_display = ('cnt_ide', 'cnt_name', )
    list_display_links = ('cnt_ide', 'cnt_name', )
    search_fields = ('cnt_name', )


@admin.register(RftOperation)
class RftOperationAdmin(admin.ModelAdmin):
    list_display = ('o_code', 'o_name', 'o_description', 'transp_type',)
    list_display_links = ('o_code', 'o_name', 'o_description', )
    search_fields = ('o_code', 'o_name', )


@admin.register(RftCargoEtsng)
class RftCargoEtsngAdmin(admin.ModelAdmin):
    list_display = ('crg_code', 'crg_name', 'update_date')
    list_display_links = ('crg_code', 'crg_name')
    search_fields = ('crg_code', 'crg_name')


@admin.register(RftRailway)
class RftRailwayAdmin(admin.ModelAdmin):
    list_display = ('rlw_code', 'rlw_name', 'rlw_full_name',
                    'cntr_ide', 'update_date', )
    list_display_links = ('rlw_code', 'rlw_name', 'rlw_full_name')
    search_fields = ('rlw_code', 'rlw_name', 'rlw_full_name')


@admin.register(RftRlwDep)
class RftRlwDepAdmin(admin.ModelAdmin):
    list_display = ('rdep_ide',
                    'rdep_code',
                    'rdep_name',
                    'rdep_full_name',
                    'rlw_code',
                    'update_date')
    list_display_links = ('rdep_ide',
                          'rdep_code',
                          'rdep_name',
                          'rdep_full_name')
    search_fields = ('rlw_code',
                     'rlw_name',
                     'rlw_full_name')


@admin.register(RftStation)
class RftStationAdmin(admin.ModelAdmin):
    list_display = ('st_code',
                    'st_code_6',
                    'st_full_name',
                    'rlw_code',
                    'rdep_ide',
                    'cntr_ide',
                    'update_date')
    list_display_links = ('st_code',
                          'st_full_name',
                          'st_code_6')
    search_fields = ('st_code', 'st_full_name', 'st_code_6')
