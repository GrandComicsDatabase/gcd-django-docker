import django

django.setup()

from apps.gcd.models import Issue
from apps.indexer.models import User
from apps.oi import states
from apps.oi.models import Changeset, IssueCreditRevision, \
                           StoryRevision, StoryCreditRevision, \
                           StoryCharacterRevision, PublisherCodeNumberRevision
from apps.oi.views import DISPLAY_CLASSES, REVISION_CLASSES, CTYPES


def setup_object(object, model_name, anon):
    changeset = Changeset(indexer=anon,
                          approver=anon,
                          state=states.APPROVED,
                          change_type=CTYPES[model_name])
    changeset.created = object.modified
    changeset.save()
    changeset.comments.create(commenter=anon,
                              text='This is an automatically generated change '
                                   'for development purposes.',
                              old_state=states.APPROVED,
                              new_state=states.APPROVED)
    comment = changeset.comments.all()[0]
    comment.created = object.modified
    comment.save()
    revision = REVISION_CLASSES[model_name].clone(object, changeset, fork=True)
    revision.source = object
    revision.created = object.modified
    revision.save()
    return changeset


def setup_object_class(model_name):
    anon = User.objects.get(username='anon')
    objects = DISPLAY_CLASSES[model_name].objects.order_by('id')
    print("Setting up: %s" % model_name)
    for object in objects[:350]:
        setup_object(object, model_name, anon)


def setup_issues():
    anon = User.objects.get(username='anon')
    objects = Issue.objects.order_by('id')
    print("Setting up: Issues")
    for object in objects[:500]:
        changeset = setup_object(object, 'issue', anon)
        for credit in object.active_credits:
            revision = IssueCreditRevision.clone(
              credit, changeset,
              issue_revision=changeset.issuerevisions.get(),
              fork=True)
            revision.source = credit
            revision.created = credit.modified
            revision.save()
        for story in object.active_stories():
            story_revision = StoryRevision.clone(story, changeset, fork=True)
            story_revision.source = story
            story_revision.created = story.modified
            story_revision.save()
            for credit in story.active_credits:
                revision = StoryCreditRevision.clone(
                  credit, changeset, story_revision=story_revision, fork=True)
                revision.source = credit
                revision.created = credit.modified
                revision.save()
            for character in story.active_characters:
                revision = StoryCharacterRevision.clone(
                  character, changeset, story_revision=story_revision,
                  fork=True)
                revision.source = character
                revision.created = character.modified
                revision.save()
            # uncomment after character/group update is deployed
            # for group in story.active_groups:
            #     revision = StoryGroupRevision.clone(
            #       group, changeset, story_revision=story_revision, fork=True)
            #     revision.source = group
            #     revision.created = group.modified
            #     revision.save()
        for code_number in object.active_code_numbers():
            revision = PublisherCodeNumberRevision.clone(
              code_number, changeset, fork=True,
              issue_revision=changeset.issuerevisions.get())
            revision.source = code_number
            revision.created = code_number.modified
            revision.save()


def main():
    # by default only first 500,
    # edit the routine if all or specific objects should be editable
    setup_object_class('publisher')
    setup_object_class('brand')
    setup_object_class('indicia_publisher')
    setup_object_class('series')
    setup_object_class('brand_group')
    setup_object_class('brand_use')
    # setup_object_class('series_bond')
    # setup_object_class('creator') # CreatorNameDetails, birth/death dates
    setup_object_class('creator_art_influence')
    setup_object_class('received_award')
    setup_object_class('creator_degree')
    setup_object_class('creator_membership')
    # setup_object_class('creator_non_comic_work')
    setup_object_class('creator_relation')
    setup_object_class('creator_school')
    setup_object_class('award')
    setup_object_class('feature')
    setup_object_class('feature_logo')
    setup_object_class('feature_relation')
    setup_object_class('printer')
    setup_object_class('indicia_printer')
    # setup_object_class('character') # CharacterNameDetails
    setup_object_class('group')
    setup_object_class('group_membership')
    setup_object_class('character_relation')
    setup_object_class('group_relation')
    setup_object_class('universe')

    # by default only first 500,
    # edit the routine if all or specific issues should be editable
    setup_issues()


if __name__ == '__main__':
    django.setup()
    main()
