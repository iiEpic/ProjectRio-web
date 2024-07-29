from api import forms, models


def get_all_objects(model_name):
    if model_name is None:
        return None
    # Check if that model exists
    if hasattr(models, model_name):
        # It does
        return getattr(models, model_name).objects.all()
    else:
        # It does not
        return None


def get_all_objects_json(model_name):
    objects_list = get_all_objects(model_name)
    if objects_list is not None:
        json_list = [i.to_json() for i in objects_list]
        return json_list
    else:
        return None


def generic_get_request_json(model_name, **kwargs):
    try:
        if kwargs['name'][-1] == '/':
            kwargs['name'] = kwargs['name'][:-1]
    except IndexError:
        # Chances are the kwargs is empty, continue as normal
        pass
    if kwargs['name'].lower() in ['', 'all']:
        return {'endpoint': kwargs['request'].path,
                'results': get_all_objects_json(model_name)
                }
    else:
        model_object = getattr(models, model_name).objects.filter(name__iexact=kwargs['name']).first()
        if model_object is not None:
            return {'endpoint': kwargs['request'].path,
                    'results': model_object.to_json()
                    }
        else:
            if kwargs['name'].isnumeric():
                model_object = getattr(models, model_name).objects.filter(pk=kwargs['name']).first()
                if model_object is not None:
                    return {'endpoint': kwargs['request'].path,
                            'results': model_object.to_json()
                            }
            return {'endpoint': kwargs['request'].path,
                    'results': 'error',
                    'error_code': f'{model_name.upper()}_NULL',
                    'error': f"{model_name} requested does not exist, {kwargs['name']}"
                    }


def generic_post_request_json(model_name, **kwargs):
    if hasattr(forms, f'{model_name}Form'):
        form = getattr(forms, f'{model_name}Form')(kwargs['request'].POST)
        if form.is_valid():
            return globals()[f'create_{model_name.lower()}'](form, kwargs['request'])
        else:
            return {'endpoint': kwargs['request'].path,
                    'results': 'error',
                    'error_code': f'{model_name.upper()}_INVALID_FORM',
                    'error': f"Data provided is not valid for creation of, {model_name}",
                    'form_errors': form.errors,
                    'required_fields': list(form.fields.keys())
                    }
    else:
        return {'endpoint': kwargs['request'].path,
                'results': 'error',
                'error_code': f'{model_name.upper()}_FORM_NOT_FOUND',
                'error': f"Internal error. Please contact administrator with this entire output.",
                'extra_info': {
                        'model_name': model_name,
                        'form_name': f'{model_name}Form'
                    }
                }


def create_tag(form, request):
    # Check if tag already exists with that name
    tag_object = models.Tag.objects.filter(name=form.cleaned_data['name']).first()
    if tag_object is not None:
        return {'endpoint': request.path,
                'results': 'error',
                'error_code': f'TAG_EXISTING',
                'error': f"A Tag with that name already exists, {form.cleaned_data['name']}",
                }
    tag_object = models.Tag.objects.create(
        name=form.cleaned_data['name'],
        tag_type=form.cleaned_data['type'],
        desc=form.cleaned_data['description']
    )
    return {'endpoint': request.path,
            'results': tag_object.to_json()
            }


def create_tagset(form, request):
    # Check if tagset already exists with that name
    tagset_object = models.TagSet.objects.filter(name=form.cleaned_data['name']).first()
    if tagset_object is not None:
        return {'endpoint': request.path,
                'results': 'error',
                'error_code': f'TAGSET_EXISTING',
                'error': f"A TagSet with that name already exists, {form.cleaned_data['name']}",
                }

    tags_list = []
    # Check if all tags provided actual exists
    for tag in form.cleaned_data['tags']['tags']:
        # Check if these tags exist by name
        tag_object = models.Tag.objects.filter(name=tag).first()
        if tag_object is not None:
            if tag_object not in tags_list:
                tags_list.append(tag_object)
        else:
            # Check if they user provided the tag ID
            tag_object = models.Tag.objects.filter(pk=tag).first()
            if tag_object is not None:
                if tag_object not in tags_list:
                    tags_list.append(tag_object)
            else:
                return {'endpoint': request.path,
                        'results': 'error',
                        'error_code': f'TAGSET_NULL_TAG',
                        'error': f"The tag, {tag}, is not a valid Tag. Use a Tags ID or Name",
                        }

    # Get community object
    community_object = models.Community.objects.filter(pk=int(form.cleaned_data['community_id'])).first()
    if community_object is None:
        return {'endpoint': request.path,
                'results': 'error',
                'error_code': f'TAGSET_COMMUNITY_NOT',
                'error': f"The community ID provided, {form.cleaned_data['community_id']}, does not exist",
                }

    return {}

    # Determine if community ID given is private
    if community_object.private:
        # Community is private, verify this user has access to it as an admin
        rio_user = models.RioUser.objects.filter(user=request.user).first()
        community_user_object = models.CommunityUser.objects.filter(community=community_object, user='')
        print('private')

    return {}
    # community_id = forms.IntegerField(label='Community ID')
    #     tags = forms.JSONField(label='Tags List')
    #     name = forms.CharField(label='Name', max_length=120)
    #     type = forms.CharField(label='type', max_length=120)
    #     start_date = forms.DateTimeField(label='Start Date')
    #     end_date = forms.DateTimeField(label='End Date')

    tagset_object = models.TagSet(
        community_id=form.cleaned_data['community_id'],
        name=form.cleaned_data['name'],
        type=form.cleaned_data['type'],
        start_date=form.cleaned_data['start_date'],
        end_date=form.cleaned_data['end_date']
    )
    return {'endpoint': path,
            'results': tagset_object.to_json()
            }


def create_community(form, path):
    print(form.cleaned_data['name'])
    print(form.cleaned_data['sponsor_id'])
    print(form.cleaned_data['community_type'])
    print(form.cleaned_data['private'])
    print(form.cleaned_data['description'])
    # Check if community already exists with that name
    community_object = models.Community.objects.filter(name=form.cleaned_data['name']).first()
    if community_object is not None:
        return {'endpoint': path,
                'results': 'error',
                'error_code': f'COMMUNITY_EXISTING',
                'error': f"A Community with that name already exists, {form.cleaned_data['name']}",
                }
    rio_user = models.RioUser.objects.filter(pk=form.cleaned_data['sponsor_id']).first()
    if rio_user is None:
        return {'endpoint': path,
                'results': 'error',
                'error_code': f'COMMUNITY_NULL_SPONSOR',
                'error': f"Sponsor with ID, {form.cleaned_data['sponsor_id']}, does not exist",
                }
    community_object = models.Community(
        name=form.cleaned_data['name'],
        sponsor=form.cleaned_data['type'],
        desc=form.cleaned_data['description']
    )
    return {'endpoint': path,
            'results': tag_object.to_json()
            }
