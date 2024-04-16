# default get,post method overriding, modelviewset, apiview, vieswset.

from rest_framework import serializers

from CarDekho_app.models import Carlist, Showroomlist, Review


class ReviewSerializer(serializers.ModelSerializer):
    apiuser = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Review
        exclude = ('car',)
        # fields = '__all__'


class CarSerializer(serializers.ModelSerializer):
    discounted_price = serializers.SerializerMethodField()
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Carlist
        fields = '__all__'

    def validate_price(self, value):
        if value <= 20000:
            raise serializers.ValidationError(
                'Price should be greater than 2000')
        return value

    def validate(self, data):
        if data['name'] == data['description']:
            raise serializers.ValidationError(
                'Name and description must not b e equal')
        return data

    def get_discounted_price(self, object):
        if object.price is not None:
            discount = object.price - 50000
            return discount
        return 100000


class ShowroomSerializer(serializers.ModelSerializer):
    # showrooms = CarSerializer(many=True, read_only=True, required=False)
    # showrooms = serializers.StringRelatedField(many=True, read_only=True)
    # showrooms = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    showrooms = serializers.HyperlinkedRelatedField(
        many=True, view_name='car_detail', read_only=True)
    # showrooms = serializers.SlugRelatedField(
    #     many=True, read_only=True, slug_field='description')
    # showrooms = serializers.HyperlinkedIdentityField(
    #     many=True, read_only=True, view_name='showroom')

    class Meta:
        model = Showroomlist
        fields = '__all__'
