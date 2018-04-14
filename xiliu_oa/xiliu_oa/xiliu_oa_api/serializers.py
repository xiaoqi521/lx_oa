# -*- coding: utf-8 -*-
from rest_framework import serializers

from django.utils import timezone

from libs.timestamp_tools.timestamp_util import str_to_standard_timestamp

from wework_core.models import User, Booking, ConferenceRoom, TimeSlot, Location, Amenity, Address, Company, \
    SupportCategory, DailyDesk, DeskSlot, DeskBooking, City
from admin_api.models import Advertisement

import logging
import traceback


class TimeStampField(serializers.Field):
    def to_representation(self, value):
        try:
            timestamp = str_to_standard_timestamp(str(timezone.localtime(value)))
            timestamp = "%f" % float(timestamp)
        except:
            logging.exception(traceback.format_exc())
            return "0"
        return timestamp


class AddressCitySerializer(serializers.ModelSerializer):

    class Meta:
        model = Address
        fields = ('id',
                  'city',
                  'line1',
                  'local_line1')


class LocationCitySerializer(serializers.ModelSerializer):

    address = AddressCitySerializer()

    class Meta:
        model = Location
        fields = ('id',
                  'name',
                  'address')


class CityListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Address
        fields = ('state',
                  'local_city')


class StateListSerializer(serializers.ModelSerializer):
    def get_nameZh(self, obj):
        return obj.name_chinese
    def get_nameEn(self, obj):
        return obj.name

    nameEn = serializers.SerializerMethodField()
    nameZh = serializers.SerializerMethodField()

    class Meta:
        model = Location
        fields = ('id',
                  'nameEn',
                  'nameZh')


class UserCompactSerializer(serializers.ModelSerializer):
    base_location = LocationCitySerializer()

    class Meta:
        model = User
        fields = ('id',
                  'name',
                  'nickname',
                  'avatar_url',
                  'base_location')


class UserAccountSerializer(serializers.ModelSerializer):
    def get_city(self, obj):

        return obj.base_location.address.city

    city = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id',
                  'name',
                  'nickname',
                  'preffered_floor',
                  'avatar_url',
                  'city',
                  'base_location')


class UserLocationSerializer(serializers.ModelSerializer):

    base_location = LocationCitySerializer()

    class Meta:
        model = User
        fields = ('id',
                  'base_location')


class TimeSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeSlot
        fields = ('type',
                  'is_peak',
                  'credit',
                  'date',
                  'occupied')


class LocationNameSerializer(serializers.ModelSerializer):
    address = AddressCitySerializer()

    class Meta:
        model = Location
        fields = ('id',
                  'uuid',
                  'digit_id',
                  'description',
                  'country',
                  'name',
                  'notes',
                  'time_zone',
                  'address',
                  'booking_notes')


class AmenitiesNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenity
        fields = ('id',
                  'name',
                  'display_name')


class ConferenceRoomSerializer(serializers.ModelSerializer):
    def get_is_preffered(self, obj):
        if 'preffered_floor' in self.context:
            if int(obj.floor) == self.context['preffered_floor']:
                return True
            else:
                return False
        else:
            return False

    location = LocationNameSerializer()

    is_preffered = serializers.SerializerMethodField()

    amenities = AmenitiesNameSerializer(many=True)

    class Meta:
        model = ConferenceRoom
        fields = ('id',
                  'uuid',
                  'name',
                  'capacity',
                  'notes',
                  'image_url',
                  'specialty',
                  'amenities',
                  'location',
                  'floor',
                  'booking_notice',
                  'large',
                  'is_preffered')


class BookingSerializer(serializers.ModelSerializer):

    start = TimeStampField()
    finish = TimeStampField()

    start_time = TimeStampField()
    end_time = TimeStampField()

    conference_room = ConferenceRoomSerializer()

    class Meta:
        model = Booking
        fields = ('user',
                  'digit_id',
                  'uuid',
                  'start',
                  'finish',
                  'notes',
                  'conference_room',
                  'credits',
                  'start_time',
                  'end_time')


class CompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = Company
        fields = ('id',
                  'uuid',
                  'name',
                  'industry',
                  'location',
                  'avatar_url')


class CompanyNameSerializer(serializers.ModelSerializer):

    class Meta:
        model = Company
        fields = ('id',
                  'uuid',
                  'name')


class SupportCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = SupportCategory
        fields = ('id',
                  'label',
                  'local_label',
                  'value',
                  'count')


class DailyDeskSerializer(serializers.ModelSerializer):

    location = LocationCitySerializer()

    class Meta:
        model = DailyDesk
        fields = ('id',
                  'uuid',
                  'digit_id',
                  'capacity',
                  'credits',
                  'notes',
                  'image_url',
                  'seats_available',
                  'location',
                  'district',
                  'after_hours_enabled',
                  'booking_notice',
                  'header_image_url')


class DeskBookingSerializer(serializers.ModelSerializer):

    start = TimeStampField()

    daily_desk = DailyDeskSerializer

    class Meta:
        model = DeskBooking
        fields = ('user',
                  'digit_id',
                  'uuid',
                  'start',
                  'daily_desk',
                  'notes',
                  'credits')


class FrontAdvertisementSerializer(serializers.ModelSerializer):
    start_time = TimeStampField()
    end_time = TimeStampField()

    class Meta:
        model = Advertisement
        fields = ('id',
                  'rank',
                  'image_name',
                  'image_url',
                  'redirect_address',
                  'start_time',
                  'end_time',
                  'disabled')


class BuildGuideSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id',
                  'wifi_name',
                  'wifi_password',
                  'print_id',
                  'print_pin',
                  'address')