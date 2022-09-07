from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.models import User, Group, Permission

# from resturant.models import Resturant_Employee_Day_Meal
# from baseInfo.models import Company, Department, Employee



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')

class UserExSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'is_active')

class UserGroupSerializer(serializers.ModelSerializer):
    groups = serializers.PrimaryKeyRelatedField(many=True, queryset=Group.objects.all())
    
    class Meta:
        model = User    
        fields = ['id', 'groups']


class GroupPermissionSerializer(serializers.ModelSerializer):
    permissions = serializers.PrimaryKeyRelatedField(many=True, queryset=Permission.objects.all())
    
    class Meta:
        model = User    
        fields = ['id', 'permissions']


class UserPermissionSerializer(serializers.ModelSerializer):
    user_permissions = serializers.PrimaryKeyRelatedField(many=True, queryset=Permission.objects.all())
    
    class Meta:
        model = User    
        fields = ['id', 'user_permissions']

# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'],
        validated_data['email'], validated_data['password'])

        return user


# Login Serializer
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Have Incorrect Credentials")


class PasswordSerializer(serializers.Serializer):
    userid = serializers.IntegerField()
    username = serializers.CharField()
    currentpassword = serializers.CharField()
    newpassword = serializers.CharField()

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass
        # instance.userid = validated_data.get('userid', instance.userid)
        # instance.password = validated_data.get('hashedNewPassword', instance.password)
        # instance.save()
        # return instance

    def validate(self, data):
        """ check that userid and new password are different """
        if data["username"] == data["newpassword"]:
            raise serializers.ValidationError("username and new password should be different")
        return data

    def validate_password(self, value):
        """
        check if new password meets the specs
        min 1 lowercase and 1 uppercase alphabet
        1 number
        1 special character
        8-16 character length
        """

        if len(value) < 8 or len(value) > 16:
            raise serializers.ValidationError("It should be between 8 and 16 characters long")

        if not any(x.isupper() for x in value):
            raise serializers.ValidationError("It should have at least one upper case alphabet")

        if not any(x.islower() for x in value):
            raise serializers.ValidationError("It should have at least one lower case alphabet")

        if not any(x.isdigit() for x in value):
            raise serializers.ValidationError("It should have at least one number")

        valid_special_characters = {'@', '_', '!', '#', '$', '%', '^', '&', '*', '(', ')',
                                    '<', '>', '?', '/', '|', '{', '}', '~', ':'}

        if not any(x in valid_special_characters for x in value):
            raise serializers.ValidationError("It should have at least one special character")

        return value


###############
# class Resturant_Employee_Day_MealExSerializer(serializers.ModelSerializer):
#     resturant_meal = serializers.SlugRelatedField(
#         read_only=True,
#         slug_field='resturant_meal'
#      )
#     date = serializers.SlugRelatedField(
#         read_only=True,
#         slug_field='date'
#      )
#     class Meta:
#         model = Resturant_Employee_Day_Meal
#         fields = ('id', 'employee', 'resturant_day_meal', 'resturant_meal', 'date')
###############

# # =======================================================
# class CompanyNameSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Company
#         fields = 'name'
        
# class DepartmentBriefSerializer(serializers.ModelSerializer):
#     # company = CompanyNameSerializer()
#     company = serializers.SlugRelatedField(
#         read_only=True,
#         slug_field='name'
#     )
#     class Meta:
#         model = Department
#         fields = 'company'

# class EmployeeBriefSerializer(serializers.ModelSerializer):
#     department = DepartmentBriefSerializer()
#     class Meta:
#         model = Employee
#         fields = ('first_name', 'last_name', 'personel_code', 'department')

# class Resturant_Fish_MealSerializer(serializers.ModelSerializer):
#     employee = EmployeeBriefSerializer()

#     resturant_meal = serializers.SlugRelatedField(
#         read_only=True,
#         slug_field='name'
#     )

#     class Meta:
#         model = Resturant_Employee_Day_Meal
#         fields = ('resturant_meal', 'employee')   
# # =======================================================        
