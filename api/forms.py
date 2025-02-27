from django import forms


class TagForm(forms.Form):
    name = forms.CharField(label='Name', max_length=32)
    type = forms.CharField(label='Tag Type', max_length=16)
    description = forms.CharField(label='Description', max_length=300)
    community_id = forms.IntegerField(label='Community ID')


class TagSetForm(forms.Form):
    community_id = forms.IntegerField(label='Community ID')
    tags = forms.JSONField(label='Tags List')
    name = forms.CharField(label='Name', max_length=120)
    type = forms.CharField(label='type', max_length=120)
    start_date = forms.DateTimeField(label='Start Date')
    end_date = forms.DateTimeField(label='End Date')


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
