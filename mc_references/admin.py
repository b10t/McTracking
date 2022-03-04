from django.contrib import admin

from .models import (RftCargoEtsng, RftContOwner, RftContType, RftCountry,
                     RftDepo, RftFirmCode, RftOperation, RftRailway,
                     RftRepairType, RftRlwDep, RftRwcCnd, RftRwcFault,
                     RftRwcGroup, RftRwcModel, RftRwcOwner, RftRwcType,
                     RftServiceType, RftStation, RwcFaultCause)


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


@admin.register(RftDepo)
class RftDepoAdmin(admin.ModelAdmin):
    list_display = ('dp_code', 'dp_name', 'dp_update_date')
    list_display_links = ('dp_code', 'dp_name')
    search_fields = ('dp_code', 'dp_name')


@admin.register(RftRwcType)
class RftRwcTypeAdmin(admin.ModelAdmin):
    list_display = ('rt_code', 'rt_name', 'update_date')
    list_display_links = ('rt_code', 'rt_name')
    search_fields = ('rt_code', 'rt_name')


@admin.register(RftRwcModel)
class RftRwcModelAdmin(admin.ModelAdmin):
    list_display = ('rm_code', 'rm_osob', 'update_date')
    list_display_links = ('rm_code', 'rm_osob')
    search_fields = ('rm_code', 'rm_osob')


@admin.register(RftContType)
class RftContTypeAdmin(admin.ModelAdmin):
    list_display = ('ct_code', 'ct_name', 'update_date')
    list_display_links = ('ct_code', 'ct_name')
    search_fields = ('ct_code', 'ct_name')


@admin.register(RftRepairType)
class RftRepairTypeAdmin(admin.ModelAdmin):
    list_display = ('rpt_code', 'rpt_name', 'update_date')
    list_display_links = ('rpt_code', 'rpt_name')
    search_fields = ('rpt_code', 'rpt_name')


@admin.register(RftRwcFault)
class RftRwcFaultAdmin(admin.ModelAdmin):
    list_display = ('flt_code', 'flt_name', 'update_date')
    list_display_links = ('flt_code', 'flt_name')
    search_fields = ('flt_code', 'flt_name')


@admin.register(RwcFaultCause)
class RwcFaultCauseAdmin(admin.ModelAdmin):
    list_display = ('cause_ide', 'cause_name')
    list_display_links = ('cause_ide', 'cause_name')
    search_fields = ('cause_ide', 'cause_name')


@admin.register(RftServiceType)
class RftServiceTypeAdmin(admin.ModelAdmin):
    list_display = ('srvt_ide', 'srvt_name')
    list_display_links = ('srvt_ide', 'srvt_name')
    search_fields = ('srvt_ide', 'srvt_name')


@admin.register(RftRwcCnd)
class RftRwcCndAdmin(admin.ModelAdmin):
    list_display = ('cnd_code', 'cnd_name')
    list_display_links = ('cnd_code', 'cnd_name')
    search_fields = ('cnd_code', 'cnd_name')


@admin.register(RftRwcGroup)
class RftRwcGroupAdmin(admin.ModelAdmin):
    list_display = ('rwc_group',
                    'rwc_group_name',
                    'rwc_parent_group',
                    'rwc_top_group',
                    'update_date')
    list_display_links = ('rwc_group', 'rwc_group_name', 'rwc_parent_group')
    search_fields = ('rwc_group', 'rwc_group_name')


@admin.register(RftRwcOwner)
class RftRwcOwnerAdmin(admin.ModelAdmin):
    list_display = ('owner_no', 'owner_name', 'parent_owner_no', 'update_date')
    list_display_links = ('owner_no', 'owner_name')
    search_fields = ('owner_no', 'owner_name')


@admin.register(RftContOwner)
class RftContOwnerAdmin(admin.ModelAdmin):
    list_display = ('cont_owner_code', 'cont_owner_name')
    list_display_links = ('cont_owner_code', 'cont_owner_name')
    search_fields = ('cont_owner_code', 'cont_owner_name')
