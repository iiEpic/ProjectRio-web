import string
from django import forms
from api.models import Community, CommunityUser


class TagForm(forms.Form):
    name = forms.CharField(label='Name', max_length=32)
    tag_type = forms.CharField(label='Tag Type', max_length=16)
    description = forms.CharField(label='Description', max_length=300)
    community_name = forms.CharField(label='Name', max_length=255)
    gecko_code = forms.CharField(widget=forms.Textarea, required=False)
    gecko_code_desc = forms.CharField(widget=forms.Textarea, required=False)

    def clean(self):
        cleaned_data = super().clean()
        tag_type = cleaned_data.get('tag_type')
        gecko_code = cleaned_data.get('gecko_code')
        if tag_type == 'Gecko Code':
            if gecko_code is None:
                self.add_error('gecko_code', 'This field is required when type is Gecko Code.')
                return

            cleaned_code = gecko_code.replace('\r', '').replace('\n', '')
            line_length = 17
            lines = [cleaned_code[i:i + line_length] for i in range(0, len(cleaned_code), line_length)]

            for line in lines:
                if len(line) != line_length:
                    self.add_error('gecko_code', 'Gecko Code is not properly formatted. '
                                                 'Lines should be 17 characters long.')
                    return

                if line[8] != ' ':
                    self.add_error('gecko_code', 'There should be a space after every 8 characters.')
                    return

                for i, char in enumerate(line):
                    if i == 8:
                        continue  # Skip the space
                    if char not in string.hexdigits:
                        self.add_error('gecko_code', 'Gecko Code is not in hexadecimal format.')
                        return


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
