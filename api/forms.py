import string
from django import forms
from api.models import Community, CommunityUser, Tag


class TagForm(forms.ModelForm):
    community_slug = forms.ChoiceField(
        label='Community Slug',
        choices=[('', '---')],
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
    hidden_community_slug = forms.CharField(widget=forms.HiddenInput(), required=False)
    tag_type = forms.ChoiceField(
        label='Tag Type',
        choices=[('component', 'Component'), ('gecko_code', 'Gecko Code')],
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    name = forms.CharField(label='Name', max_length=32, widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(
        label='Description', max_length=300, widget=forms.TextInput(attrs={'class': 'form-control'}), required=False
    )
    gecko_code = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'style': 'min-height: 150px;'}), required=False
    )
    gecko_code_desc = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)

    class Meta:
        model = Tag
        fields = ['name', 'tag_type', 'description', 'gecko_code', 'gecko_code_desc']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        communities = Community.objects.all()
        community_choices = [('', '---')] + [(community.slug, community.name) for community in communities]
        self.fields['community_slug'].choices = community_choices
        if self.instance and self.instance.community:
            self.fields['community_slug'].initial = self.instance.community.slug
            self.fields['hidden_community_slug'].initial = self.instance.community.slug
            if self.instance.pk:
                self.fields['community_slug'].widget.attrs['disabled'] = True
                self.fields['name'].widget.attrs['disabled'] = True
                self.fields['active'] = forms.BooleanField(label='Active')
                self.fields['active'].widget.attrs['class'] = 'form-check-input'
                self.fields['active'].widget.attrs['type'] = 'checkbox'
                self.fields['active'].widget.attrs['role'] = 'switch'
                self.fields['active'].widget.attrs['id'] = 'active'
                self.fields['active'].widget.attrs['checked'] = self.instance.active

    def is_valid(self, *args, **kwargs):

        if 'edit' in self.data and self.data['edit']:

            request = self.data['request']
            self.data.pop('edit')

            # This is a modification of an existing
            self.errors.clear()

            # Check if the tag we are requesting actually exists
            tag_object = Tag.objects.filter(slug__iexact=self.data.get('slug')).first()
            if tag_object is None:
                self.add_error('name', 'Tag does not exist by that name.')
            else:
                self.data['name'] = tag_object.name

            if 'community_slug' in self.cleaned_data:
                community_slug = self.cleaned_data['community_slug']
                self.cleaned_data.pop('community_slug')
            else:
                community_slug = self.cleaned_data['hidden_community_slug']
                self.cleaned_data.pop('hidden_community_slug')

            self.cleaned_data['community'] = Community.objects.filter(slug__iexact=community_slug).first()

            # Check if the community we are requesting actually exists
            if self.cleaned_data['community'] is None:
                self.add_error('community_slug', 'Community does not exist by that slug.')

            community_user = CommunityUser.objects.filter(
                community=self.cleaned_data['community'],
                user=request.user
            ).first()
            # The following is being checked:
            # - Community exists by the name the user gave
            # - CommunityUser exists for the community given and user trying to post
            # - CommunityUser is an admin in that Community
            # Check if the user has access to add a Tag to this community, and they didn't forge the post request
            if not request.user.is_staff and (self.cleaned_data[
                                                       'community'] is None or community_user is None):
                self.add_error('community_slug', 'Could not find a community with that name')

            if not request.user.is_staff and (community_user is None or community_user.role.name != 'Admin'):
                self.add_error('description', 'You do not have permissions to edit this Tag. '
                                              'Please ask a Community Admin.')

            if self.cleaned_data['tag_type'] == 'component' or self.cleaned_data['gecko_code'] == '':
                self.cleaned_data['gecko_code'] = None
                self.cleaned_data['gecko_code_desc'] = None

            if 'active' in self.data:
                self.cleaned_data['active'] = True if self.data['active'] in ['on', 'True'] else False

            if self.errors:
                print(self.errors)
                return False
            else:
                self.cleaned_data.pop('community')
                return True
        else:
            # This is a new creation
            return super().is_valid()

    def clean(self):
        cleaned_data = super().clean()
        tag_type = cleaned_data.get('tag_type')
        gecko_code = cleaned_data.get('gecko_code')
        if tag_type == 'gecko_code':
            if not gecko_code:
                self.add_error('gecko_code', 'This field is required when type is Gecko Code.')
                return cleaned_data

            cleaned_code = gecko_code.replace('\r', '').replace('\n', '')
            line_length = 17
            lines = [cleaned_code[i:i + line_length] for i in range(0, len(cleaned_code), line_length)]

            for line in lines:
                if len(line) != line_length:
                    self.add_error('gecko_code', 'Gecko Code is not properly formatted. Lines should be 17 characters long.')
                    return cleaned_data

                if line[8] != ' ':
                    self.add_error('gecko_code', 'There should be a space after every 8 characters.')
                    return cleaned_data

                for i, char in enumerate(line):
                    if i == 8:
                        continue  # Skip the space
                    if char not in string.hexdigits:
                        self.add_error('gecko_code', 'Gecko Code is not in hexadecimal format.')
                        return cleaned_data

        return cleaned_data


class TagPatchForm(forms.ModelForm):
    community_slug = forms.CharField(label='Community Slug', max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
    hidden_community_slug = forms.CharField(widget=forms.HiddenInput(), required=False)
    tag_type = forms.ChoiceField(
        label='Tag Type',
        choices=[('component', 'Component'), ('gecko_code', 'Gecko Code')],
        widget=forms.Select(attrs={'class': 'form-select'}),
        required=False
    )
    name = forms.CharField(label='Name', max_length=32, widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(label='Description', max_length=300, widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    gecko_code = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'style': 'min-height: 150px;'}), required=False
    )
    gecko_code_desc = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)

    class Meta:
        model = Tag
        fields = ['name', 'tag_type', 'description', 'gecko_code', 'gecko_code_desc']

    def is_valid(self, *args, **kwargs):
        self.errors.clear()

        # Check if the tag we are requesting actually exists
        if Tag.objects.filter(name__iexact=self.data.get('name')).first() is None:
            self.add_error('name', 'Tag does not exist by that name.')

        # Check if the community we are requesting actually exists
        if Community.objects.filter(slug__iexact=self.data.get('community_slug')).first() is None:
            self.add_error('community_slug', 'Community does not exist by that slug.')

        if self.errors:
            return False
        else:
            self.cleaned_data['name'] = self.data.get('name')
            return True

    def clean(self):
        cleaned_data = super().clean()
        tag_type = cleaned_data.get('tag_type')
        gecko_code = cleaned_data.get('gecko_code')
        if tag_type == 'gecko_code':
            if not gecko_code:
                self.add_error('gecko_code', 'This field is required when type is Gecko Code.')
                return cleaned_data

            cleaned_code = gecko_code.replace('\r', '').replace('\n', '')
            line_length = 17
            lines = [cleaned_code[i:i + line_length] for i in range(0, len(cleaned_code), line_length)]

            for line in lines:
                if len(line) != line_length:
                    self.add_error('gecko_code', 'Gecko Code is not properly formatted. Lines should be 17 characters long.')
                    return cleaned_data

                if line[8] != ' ':
                    self.add_error('gecko_code', 'There should be a space after every 8 characters.')
                    return cleaned_data

                for i, char in enumerate(line):
                    if i == 8:
                        continue  # Skip the space
                    if char not in string.hexdigits:
                        self.add_error('gecko_code', 'Gecko Code is not in hexadecimal format.')
                        return cleaned_data

        return cleaned_data


class TagSetForm(forms.Form):
    community_name = forms.CharField(label='Community Name', max_length=120)
    tags = forms.CharField(label='Tags', max_length=255)
    name = forms.CharField(label='Name', max_length=120)
    tagset_type = forms.CharField(label='Tagset Type', max_length=120)  # Season, League, or Tournament
    start_date = forms.DateTimeField(label='Start Date')
    end_date = forms.DateTimeField(label='End Date')

    def clean(self):
        cleaned_data = super().clean()
        tagset_type = cleaned_data.get('tagset_type')
        if tagset_type not in ['League', 'Season', 'Tournament']:
            self.add_error('tagset_type', 'Only types allowed are: [League, Season, Tournament]')


class CommunityForm(forms.Form):
    name = forms.CharField(label='Name', max_length=32)
    community_type = forms.CharField(label='Community Type', max_length=16)
    private = forms.IntegerField(label='Private')
    global_link = forms.IntegerField(label='Global Link', required=False)
    description = forms.CharField(label='Description', max_length=300, required=False)


class PopulateDBForm(forms.Form):
    average_ping = forms.IntegerField(label='Average Ping')
    away_player = forms.CharField(label='Away Player', max_length=300)
    away_score = forms.IntegerField(label='Away Score')
    date_end = forms.IntegerField(label='Date Ended')
    date_start = forms.IntegerField(label='Date Started')
    game_id = forms.CharField(label='Game ID')
    home_player = forms.CharField(label='Home Player', max_length=300)
    home_score = forms.IntegerField(label='Home Score')
    innings_played = forms.IntegerField(label='Innings Played')
    innings_selected = forms.IntegerField(label='Innings Selected')
    lag_spikes = forms.IntegerField(label='Lag Spikes')
    netplay = forms.BooleanField(label='Netplay')
    quitter = forms.CharField(label='Quitter', max_length=300)
    stadium_id = forms.IntegerField(label='Stadium ID')
    tagset_id = forms.IntegerField(label='Tagset ID')
    valid = forms.BooleanField(label='Valid')
    version = forms.CharField(label='Version', max_length='5')  # 1.0.0
