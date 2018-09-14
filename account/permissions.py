from rest_framework import permissions



class IsUserOrReadOnly(permissions.IsAuthenticated):

	
	def has_object_permission(self,request,view,obj):
		#import pdb;pdb.set_trace()
		if request.method in permissions.SAFE_METHODS:
			return True
		else:
			return obj.user == request.user

class IsLoginUserOrReadOnly(permissions.IsAuthenticated):

	
	def has_object_permission(self,request,view,obj):
		#import pdb;pdb.set_trace()
		if request.method in permissions.SAFE_METHODS:
			return True
		else:
			return obj.id == request.user.id


class IsOwnerOrReadOnly(permissions.BasePermission):

	
	def has_object_permission(self,request,view,obj):
		#import pdb;pdb.set_trace()
		if request.method in permissions.SAFE_METHODS:
			return True
		else:
			return obj.owner == request.user