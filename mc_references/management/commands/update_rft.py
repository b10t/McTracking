import os
from datetime import datetime

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils.timezone import localtime
from mc_references.models import (RftCargoEtsng, RftCountry, RftFirmCode,
                                  RftOperation, RftRailway)
from McTracking.settings import (AUTH_PASSWORD, AUTH_USER, WSDL_ADDRESS,
                                 WSDL_PASSWORD, WSDL_USER)
from pytz import timezone
from requests import Session
from requests.auth import HTTPBasicAuth
# from zeep import AsyncClient
from zeep.client import Client
from zeep.exceptions import XMLParseError
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
    if response['OUT_RESULT'] == 0:
        return response['OUT_MESSAGE']['INFO']['REF']
    return []


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
        for firm in response:
            for code in firm['CODE']:
                firm_new, _ = RftFirmCode.objects.get_or_create(
                    frc_code=code['FRC_CODE'],
                    frct_ide=int(code['FRCT_IDE']),
                    okpo=firm['OKPO'],
                    frm_short_name=firm['FRM_SHORT_NAME'],
                    frm_name=firm['FRM_NAME'],
                    update_date=convert_str_to_datetime(firm['UPDATE_DATE']))


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
        for country in response:
            country_new, _ = RftCountry.objects.get_or_create(
                cnt_ide=str(country["CNT_IDE"]).rjust(3, "0"),
                cnt_name=str(country['CNT_NAME']).capitalize(),
                update_date=convert_str_to_datetime(country['UPDATE_DATE']))


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
        for operation in response:
            operation_new, _ = RftOperation.objects.get_or_create(
                o_code=operation['O_CODE'],
                o_name=operation['O_NAME'],
                o_description=operation['O_DESCRIPTION'],
                transp_type=int(operation['TRANSP_TYPE']),
                update_date=convert_str_to_datetime(operation['UPDATE_DATE']))


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
        for cargo in response:
            cargo_new, _ = RftCargoEtsng.objects.get_or_create(
                crg_code=int(cargo['CRG_CODE']),
                crg_name=cargo['CRG_NAME'],
                update_date=convert_str_to_datetime(cargo['UPDATE_DATE']))


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
        for railway in response:
            railway_new, _ = RftRailway.objects.get_or_create(
                rlw_code=railway['RLW_CODE'],
                rlw_name=railway['RLW_NAME'],
                rlw_full_name=str(railway['RLW_FULL_NAME']).upper(),
                cntr_ide=RftCountry.objects.get(
                    pk=str(railway["CNTR_IDE"]).rjust(3, "0")),
                update_date=convert_str_to_datetime(railway['UPDATE_DATE']))


class Command(BaseCommand):
    help = 'Update RFT from SOAP.'

    def handle(self, *args, **options):
        mc_tracking_service = get_service_wsdl(AUTH_USER,
                                               AUTH_PASSWORD,
                                               WSDL_ADDRESS)

        start_time = datetime.now()
        print('Start', start_time)

        begin_date = datetime(2022, 1, 1)
        end_date = datetime(2022, 2, 15)

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
        update_rft_railway(mc_tracking_service,
                           WSDL_USER,
                           WSDL_PASSWORD,
                           begin_date,
                           end_date)

        print(datetime.now() - start_time)

        # '2019-01-01T00:00:00',
        # '2021-12-01T00:00:00',
