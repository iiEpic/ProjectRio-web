from django.contrib import admin
from api.models import *


# Register your models here.
@admin.register(ApiKey)
class ApiKeyAdmin(admin.ModelAdmin):
    pass


@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    pass


@admin.register(CharacterGameSummary)
class CharacterGameSummaryAdmin(admin.ModelAdmin):
    pass


@admin.register(CharacterPositionSummary)
class CharacterPositionSummaryAdmin(admin.ModelAdmin):
    pass


@admin.register(ChemistryTable)
class ChemistryTableAdmin(admin.ModelAdmin):
    pass


@admin.register(Community)
class CommunityAdmin(admin.ModelAdmin):
    pass


@admin.register(CommunityUser)
class CommunityUserAdmin(admin.ModelAdmin):
    pass


@admin.register(ContactSummary)
class ContactSummaryAdmin(admin.ModelAdmin):
    pass


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    pass


@admin.register(FieldingSummary)
class FieldingSummaryAdmin(admin.ModelAdmin):
    pass


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    pass


@admin.register(GameHistory)
class GameHistoryAdmin(admin.ModelAdmin):
    pass


@admin.register(GeckoCodeTag)
class GeckoCodeTagAdmin(admin.ModelAdmin):
    pass


@admin.register(Ladder)
class LadderAdmin(admin.ModelAdmin):
    pass


@admin.register(OngoingGame)
class OngoingGameAdmin(admin.ModelAdmin):
    pass


@admin.register(PitchSummary)
class PitchSummaryAdmin(admin.ModelAdmin):
    pass


@admin.register(RioUser)
class RioUserAdmin(admin.ModelAdmin):
    pass


@admin.register(Runner)
class RunnerAdmin(admin.ModelAdmin):
    pass


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass


@admin.register(TagSet)
class TagSetAdmin(admin.ModelAdmin):
    pass


@admin.register(UserGroup)
class UserGroupAdmin(admin.ModelAdmin):
    pass


@admin.register(UserGroupUser)
class UserGroupUserAdmin(admin.ModelAdmin):
    pass

