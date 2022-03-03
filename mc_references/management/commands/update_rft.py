import os
from datetime import datetime

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils.timezone import localtime
from mc_references.models import (RftCargoEtsng, RftContType, RftCountry,
                                  RftDepo, RftFirmCode, RftOperation,
                                  RftRailway, RftRepairType, RftRlwDep,
                                  RftRwcModel, RftRwcType, RftStation,
                                  RwcFaultCause)
from McTracking.settings import (AUTH_PASSWORD, AUTH_USER, WSDL_ADDRESS,
                                 WSDL_PASSWORD, WSDL_USER)
from pytz import timezone
from requests import Session
from requests.auth import HTTPBasicAuth
# from zeep import AsyncClient
from zeep.client import Client
from zeep.exceptions import XMLParseError
from zeep.helpers import serialize_object
from zeep.settings import Settings
from zeep.transports import AsyncTransport, Transport


def get_service_wsdl(auth_user, auth_password, wsdl_address):
    """Возвращает wsdl сервис.

    Returns:
        ServiceProxy: Wsdl сервис
    """
    session = Session()
    session.auth = HTTPBasicAuth(AUTH_USER, AUTH_PASSWORD)

    settings = Settings(strict=False, xsd_ignore_sequence_order=True)
    client = Client(wsdl=os.path.dirname(__file__) + '/get_data.wsdl',
                    transport=Transport(session=session),
                    settings=settings)

    return client.create_service(
        '{http://xmlns.oracle.com/orawsv/RWC_INF/GET_DATA}GET_DATABinding',
        f'http://{wsdl_address}/orawsv/RWC_INF/GET_DATA')


def get_response_from_service(response):
    info_ref_list = []

    if response['OUT_RESULT'] == 0:
        for item in response['OUT_MESSAGE']['INFO']['REF']:
            info_ref_list.append(
                convert_zeep_object_to_dict(item)
            )

    return info_ref_list


def convert_str_to_datetime(update_date):
    """Преобразовывает строку в дату с зоной МСК.

    Args:
        update_date (str): Дата строкой

    Returns:
        datetime: Дата и время с зоной МСК
    """
    msk_timezone = timezone('Europe/Moscow')

    return msk_timezone.localize(
        datetime.strptime(
            update_date,
            "%d.%m.%Y %H:%M:%S"
        )
    )


def convert_zeep_object_to_dict(zeep_objects):
    """Конвертирует данные полученные от сервиса.

    Args:
        zeep_objects (zeep.objects): Данные от сервиса

    Returns:
        dict: Обработанные данные
    """
    zeep_dict = {k.lower(): v for k, v in serialize_object(
        zeep_objects).items()
    }

    if 'update_date' in zeep_dict:
        zeep_dict['update_date'] = convert_str_to_datetime(
            zeep_dict['update_date']
        )

    if 'dp_update_date' in zeep_dict:
        zeep_dict['dp_update_date'] = convert_str_to_datetime(
            zeep_dict['dp_update_date']
        )
    return zeep_dict


def update_rft_firm_code(service,
                         wsdl_user,
                         wsdl_password,
                         begin_date,
                         end_date):
    response = get_response_from_service(
        service.GET_DATA_RFT_FIRM_CODE
        (
            begin_date,
            end_date,
            wsdl_user,
            wsdl_password,
            '',
            ''
        )
    )

    with transaction.atomic():
        for service_data in response:
            firm_codes = service_data['code']
            del service_data['code']

            for code in firm_codes:
                service_data['frc_code'] = code['FRC_CODE']
                service_data['frct_ide'] = int(code['FRCT_IDE'])

                RftFirmCode.objects.update_or_create(
                    frc_code=code['FRC_CODE'],
                    frct_ide=int(code['FRCT_IDE']),
                    okpo=service_data['okpo'],
                    defaults=service_data
                )


def update_rft_country(service,
                       wsdl_user,
                       wsdl_password,
                       begin_date,
                       end_date):
    response = get_response_from_service(
        service.GET_DATA_RFT_COUNTRY
        (
            begin_date,
            end_date,
            wsdl_user,
            wsdl_password,
            '',
            ''
        )
    )

    with transaction.atomic():
        for service_data in response:
            service_data['cnt_ide'] = str(
                service_data['cnt_ide']).rjust(3, "0")

            RftCountry.objects.update_or_create(
                cnt_ide=service_data['cnt_ide'],
                defaults=service_data
            )


def update_rft_operation(service,
                         wsdl_user,
                         wsdl_password,
                         begin_date,
                         end_date):
    response = get_response_from_service(
        service.GET_DATA_RFT_OPERATION
        (
            begin_date,
            end_date,
            wsdl_user,
            wsdl_password,
            '',
            ''
        )
    )

    with transaction.atomic():
        for service_data in response:
            service_data['transp_type'] = int(service_data['transp_type'])

            RftOperation.objects.update_or_create(
                o_code=service_data['o_code'],
                o_name=service_data['o_name'],
                transp_type=service_data['transp_type'],
                defaults=service_data
            )


def update_rft_cargo_etsng(service,
                           wsdl_user,
                           wsdl_password,
                           begin_date,
                           end_date):
    response = get_response_from_service(
        service.GET_DATA_RFT_CARGO_ETSNG
        (
            begin_date,
            end_date,
            wsdl_user,
            wsdl_password,
            '',
            ''
        )
    )

    with transaction.atomic():
        for service_data in response:
            service_data['crg_code'] = int(service_data['crg_code'])

            RftCargoEtsng.objects.update_or_create(
                crg_code=service_data['crg_code'],
                defaults=service_data
            )


def update_rft_railway(service,
                       wsdl_user,
                       wsdl_password,
                       begin_date,
                       end_date):
    response = get_response_from_service(
        service.GET_DATA_RFT_RAILWAY
        (
            begin_date,
            end_date,
            wsdl_user,
            wsdl_password,
            '',
            ''
        )
    )

    with transaction.atomic():
        for service_data in response:
            service_data['cntr_ide'] = RftCountry.get_by_id(
                service_data['cntr_ide']
            )

            RftRailway.objects.update_or_create(
                rlw_code=service_data['rlw_code'],
                defaults=service_data
            )


def update_rft_rlw_dep(service,
                       wsdl_user,
                       wsdl_password,
                       begin_date,
                       end_date):
    response = get_response_from_service(
        service.GET_DATA_RFT_RLW_DEP
        (
            begin_date,
            end_date,
            wsdl_user,
            wsdl_password,
            '',
            ''
        )
    )

    with transaction.atomic():
        for service_data in response:
            service_data['rlw_code'] = RftRailway.get_by_id(
                service_data['rlw_code'])

            RftRlwDep.objects.update_or_create(
                rdep_ide=service_data['rdep_ide'],
                defaults=service_data
            )


def update_rft_station(service,
                       wsdl_user,
                       wsdl_password,
                       begin_date,
                       end_date):
    response = get_response_from_service(
        service.GET_DATA_RFT_STATION
        (
            begin_date,
            end_date,
            wsdl_user,
            wsdl_password,
            '',
            ''
        )
    )

    with transaction.atomic():
        for service_data in response:
            service_data['rlw_code'] = RftRailway.get_by_id(
                service_data['rlw_code'])
            service_data['rdep_ide'] = RftRlwDep.get_by_id(
                service_data['rdep_ide'])
            service_data['cntr_ide'] = RftCountry.get_by_id(
                service_data['cntr_ide'])

            RftStation.objects.update_or_create(
                st_code=service_data['st_code'],
                defaults=service_data
            )


def update_rft_depo(service,
                    wsdl_user,
                    wsdl_password,
                    begin_date,
                    end_date):
    response = get_response_from_service(
        service.GET_DATA_RFT_DEPO
        (
            begin_date,
            end_date,
            wsdl_user,
            wsdl_password,
            '',
            ''
        )
    )

    with transaction.atomic():
        for service_data in response:
            service_data['dp_code'] = str(
                service_data['dp_code']).rjust(4, "0")

            RftDepo.objects.update_or_create(
                dp_code=service_data['dp_code'],
                defaults=service_data
            )


def update_rft_rwc_type(service,
                        wsdl_user,
                        wsdl_password,
                        begin_date,
                        end_date):
    response = get_response_from_service(
        service.GET_DATA_RFT_RWC_TYPE
        (
            begin_date,
            end_date,
            wsdl_user,
            wsdl_password,
            '',
            ''
        )
    )

    with transaction.atomic():
        for service_data in response:
            service_data['rt_code'] = str(
                service_data['rt_code']).rjust(2, "0")

            RftRwcType.objects.update_or_create(
                rt_code=service_data['rt_code'],
                defaults=service_data
            )


def update_rft_rwc_model(service,
                         wsdl_user,
                         wsdl_password,
                         begin_date,
                         end_date):
    response = get_response_from_service(
        service.GET_DATA_RFT_RWC_MODEL
        (
            begin_date,
            end_date,
            wsdl_user,
            wsdl_password,
            '',
            ''
        )
    )

    with transaction.atomic():
        for service_data in response:
            RftRwcModel.objects.update_or_create(
                rm_code=service_data['rm_code'],
                defaults=service_data
            )


def update_rft_cont_type(service,
                         wsdl_user,
                         wsdl_password,
                         begin_date,
                         end_date):
    response = get_response_from_service(
        service.GET_DATA_RFT_CONT_TYPE
        (
            begin_date,
            end_date,
            wsdl_user,
            wsdl_password,
            '',
            ''
        )
    )

    with transaction.atomic():
        for service_data in response:
            RftContType.objects.update_or_create(
                ct_code=service_data['ct_code'],
                defaults=service_data
            )


def update_rft_repait_type(service,
                           wsdl_user,
                           wsdl_password,
                           begin_date,
                           end_date):
    response = get_response_from_service(
        service.GET_DATA_RFT_REPAIR_TYPE
        (
            begin_date,
            end_date,
            wsdl_user,
            wsdl_password,
            '',
            ''
        )
    )

    with transaction.atomic():
        for service_data in response:
            RftRepairType.objects.update_or_create(
                rpt_code=service_data['rpt_code'],
                defaults=service_data
            )


def update_rft_fault_cause(service,
                           wsdl_user,
                           wsdl_password):
    response = get_response_from_service(
        service.GET_DATA_RFT_RWC_FAULT_CAUSE
        (
            wsdl_user,
            wsdl_password,
            '',
            ''
        )
    )

    with transaction.atomic():
        for service_data in response:
            RwcFaultCause.objects.update_or_create(
                cause_ide=service_data['cause_ide'],
                defaults=service_data
            )


class Command(BaseCommand):
    help = 'Update RFT from SOAP.'

    def handle(self, *args, **options):
        mc_tracking_service = get_service_wsdl(AUTH_USER,
                                               AUTH_PASSWORD,
                                               WSDL_ADDRESS)

        start_time = datetime.now()
        print('Start', start_time)

        begin_date = datetime(2021, 1, 1)
        end_date = datetime(2022, 3, 3)

        # update_rft_firm_code(mc_tracking_service,
        #                      WSDL_USER,
        #                      WSDL_PASSWORD,
        #                      begin_date,
        #                      end_date)
        # update_rft_country(mc_tracking_service,
        #                    WSDL_USER,
        #                    WSDL_PASSWORD,
        #                    begin_date,
        #                    end_date)
        # update_rft_operation(mc_tracking_service,
        #                      WSDL_USER,
        #                      WSDL_PASSWORD,
        #                      begin_date,
        #                      end_date)
        # update_rft_cargo_etsng(mc_tracking_service,
        #                        WSDL_USER,
        #                        WSDL_PASSWORD,
        #                        begin_date,
        #                        end_date)
        # update_rft_railway(mc_tracking_service,
        #                    WSDL_USER,
        #                    WSDL_PASSWORD,
        #                    begin_date,
        #                    end_date)
        # update_rft_rlw_dep(mc_tracking_service,
        #                    WSDL_USER,
        #                    WSDL_PASSWORD,
        #                    begin_date,
        #                    end_date)
        # update_rft_station(mc_tracking_service,
        #                    WSDL_USER,
        #                    WSDL_PASSWORD,
        #                    begin_date,
        #                    end_date)
        # update_rft_depo(mc_tracking_service,
        #                 WSDL_USER,
        #                 WSDL_PASSWORD,
        #                 begin_date,
        #                 end_date)
        # update_rft_rwc_type(mc_tracking_service,
        #                     WSDL_USER,
        #                     WSDL_PASSWORD,
        #                     begin_date,
        #                     end_date)
        # update_rft_rwc_model(mc_tracking_service,
        #                      WSDL_USER,
        #                      WSDL_PASSWORD,
        #                      begin_date,
        #                      end_date)
        # update_rft_cont_type(mc_tracking_service,
        #                      WSDL_USER,
        #                      WSDL_PASSWORD,
        #                      begin_date,
        #                      end_date)
        # update_rft_repait_type(mc_tracking_service,
        #                        WSDL_USER,
        #                        WSDL_PASSWORD,
        #                        begin_date,
        #                        end_date)
        update_rft_fault_cause(mc_tracking_service,
                               WSDL_USER,
                               WSDL_PASSWORD)

        print(datetime.now() - start_time)

        # '2019-01-01T00:00:00',
        # '2021-12-01T00:00:00',
