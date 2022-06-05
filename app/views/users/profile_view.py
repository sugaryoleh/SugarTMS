from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAdminUser
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from app.models.users.profile import Profile
from app.serializers.users.profile_serializer import ProfileSerializer
from app.views.base.delete_view import DeleteView
from app.views.base.detail_view import DetailView


@permission_classes([IsAdminUser])
class ProfileAdd(APIView):
    serializer = ProfileSerializer
    model = Profile
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'add.html'

    def get(self, request):

        serializer = self.serializer(context={'request': request})

        return Response({'serializer': serializer,
                         'title': self.model._meta.verbose_name.title(),
                         'view_name': '{}-add'.format(self.model._meta.verbose_name_raw),
                         })

    def post(self, request):
        serializer = self.serializer(data=request.data, context={'request': request})
        if not serializer.is_valid():
            return Response({'title': self.model._meta.verbose_name.title(),
                             'view_name': 'profile-add',
                             'serializer': serializer,
                             })
        serializer.save()
        return redirect('profile-list')


@permission_classes([IsAdminUser])
class ProfileDetail(DetailView):
    serializer = ProfileSerializer
    model = Profile
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'profile/detail.html'

    def get(self, request, pk):
        obj = get_object_or_404(self.model, pk=pk)
        user = User.objects.get(pk=obj.id)
        data = {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'is_superuser': user.is_superuser,
            'is_coordinator': obj.is_coordinator,
        }
        serializer = self.serializer(data=data, context={'request': request})
        if serializer.is_valid():
            return Response({'serializer': serializer,
                             'title': self.model._meta.verbose_name.title(),
                             'pk': pk,
                             'view_name': 'profile-detail',
                             'delete_view_name': 'profile-delete',
                             })
        return redirect('profile-list')

    def post(self, request, pk):
        obj = get_object_or_404(self.model, pk=pk)
        user = User.objects.get(pk=obj.id)
        data = {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'is_superuser': user.is_superuser,
            'is_coordinator': obj.is_coordinator,
        }
        serializer = self.serializer(data=data, context={'request': request})
        if not serializer.is_valid():
            return Response({'serializer': serializer,
                             'title': self.model._meta.verbose_name.title(),
                             'pk': pk,
                             'view_name': 'profile-detail',
                             'delete_view_name': 'profile-delete',
                             })
        serializer.update(obj, validated_data=request.data)
        return redirect('profile-list')


@permission_classes([IsAdminUser])
class ProfileDelete(DeleteView):
    serializer = ProfileSerializer
    model = Profile


@permission_classes([IsAdminUser])
class ProfileList(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'profile/list.html'
    model = Profile
    serializer = ProfileSerializer

    def get(self, request):
        users = User.objects.all()
        profiles = Profile.objects.all()
        data = []
        for profile in profiles:
            data.append((profile, users.get(pk=profile.user.id)))
        data = [{'id': profile.pk, 'first_name': user.first_name, 'last_name': user.last_name, 'email': user.email,
                 'is_superuser': user.is_superuser, 'is_coordinator': profile.is_coordinator} for profile, user in data]
        hat = ['First name', 'Last name', 'email', 'Superuser', 'Coordinator']
        return Response({'data': data,
                         'hat': hat,
                         'add_view_name': 'profile-add',
                         'detail_view_name': 'profile-detail',
                         'title': self.model._meta.verbose_name_plural.title(),
                         })
