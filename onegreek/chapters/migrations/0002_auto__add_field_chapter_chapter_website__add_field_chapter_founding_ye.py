# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Chapter.chapter_website'
        db.add_column(u'chapters_chapter', 'chapter_website',
                      self.gf('django.db.models.fields.URLField')(default='', max_length=200, blank=True),
                      keep_default=False)

        # Adding field 'Chapter.founding_year'
        db.add_column(u'chapters_chapter', 'founding_year',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Chapter.chapter_address'
        db.add_column(u'chapters_chapter', 'chapter_address',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Chapter.chapter_website'
        db.delete_column(u'chapters_chapter', 'chapter_website')

        # Deleting field 'Chapter.founding_year'
        db.delete_column(u'chapters_chapter', 'founding_year')

        # Deleting field 'Chapter.chapter_address'
        db.delete_column(u'chapters_chapter', 'chapter_address')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'chapters.chapter': {
            'Meta': {'object_name': 'Chapter'},
            u'_awards_excerpt': ('django.db.models.fields.TextField', [], {}),
            u'_description_excerpt': ('django.db.models.fields.TextField', [], {}),
            u'_philanthropy_excerpt': ('django.db.models.fields.TextField', [], {}),
            u'_potential_new_members_excerpt': ('django.db.models.fields.TextField', [], {}),
            'awards': ('model_utils.fields.SplitField', [], {u'no_excerpt_field': 'True', 'blank': 'True'}),
            'chapter_address': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'chapter_website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'cost': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'description': ('model_utils.fields.SplitField', [], {u'no_excerpt_field': 'True', 'blank': 'True'}),
            'facebook': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'fb_status': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'founding_year': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'fraternity': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['fraternities.Fraternity']", 'null': 'True', 'blank': 'True'}),
            'fraternity_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'gpa': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['auth.Group']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'linked_active_group': ('django.db.models.fields.related.OneToOneField', [], {'blank': 'True', 'related_name': "'linked_chapter_active'", 'unique': 'True', 'null': 'True', 'to': u"orm['auth.Group']"}),
            'linked_admin_group': ('django.db.models.fields.related.OneToOneField', [], {'blank': 'True', 'related_name': "'linked_chapter_admin'", 'unique': 'True', 'null': 'True', 'to': u"orm['auth.Group']"}),
            'linked_call_group': ('django.db.models.fields.related.OneToOneField', [], {'blank': 'True', 'related_name': "'linked_chapter_call'", 'unique': 'True', 'null': 'True', 'to': u"orm['auth.Group']"}),
            'linked_group': ('django.db.models.fields.related.OneToOneField', [], {'blank': 'True', 'related_name': "'linked_chapter'", 'unique': 'True', 'null': 'True', 'to': u"orm['auth.Group']"}),
            'linked_pending_group': ('django.db.models.fields.related.OneToOneField', [], {'blank': 'True', 'related_name': "'linked_chapter_pending'", 'unique': 'True', 'null': 'True', 'to': u"orm['auth.Group']"}),
            'linked_pledge_group': ('django.db.models.fields.related.OneToOneField', [], {'blank': 'True', 'related_name': "'linked_chapter_pledge'", 'unique': 'True', 'null': 'True', 'to': u"orm['auth.Group']"}),
            'linked_rush_group': ('django.db.models.fields.related.OneToOneField', [], {'blank': 'True', 'related_name': "'linked_chapter_rush'", 'unique': 'True', 'null': 'True', 'to': u"orm['auth.Group']"}),
            'location': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'philanthropy': ('model_utils.fields.SplitField', [], {u'no_excerpt_field': 'True', 'blank': 'True'}),
            'potential_new_members': ('model_utils.fields.SplitField', [], {u'no_excerpt_field': 'True', 'blank': 'True'}),
            'rush_form': ('django.db.models.fields.related.OneToOneField', [], {'blank': 'True', 'related_name': "'chapter'", 'unique': 'True', 'null': 'True', 'to': u"orm['rush_forms.Form']"}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'}),
            'status': ('model_utils.fields.StatusField', [], {'default': "'excellence'", 'max_length': '100', u'no_check_for_status': 'True'}),
            'status_changed': ('model_utils.fields.MonitorField', [], {'default': 'datetime.datetime.now', u'monitor': "u'status'"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'university': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['universities.University']", 'null': 'True', 'blank': 'True'}),
            'university_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        },
        u'chapters.position': {
            'Meta': {'object_name': 'Position'},
            'chapter': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['chapters.Chapter']"}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'fraternities.fraternity': {
            'Meta': {'object_name': 'Fraternity'},
            u'_description_excerpt': ('django.db.models.fields.TextField', [], {}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'description': ('model_utils.fields.SplitField', [], {u'no_excerpt_field': 'True', 'blank': 'True'}),
            'facebook': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'fb_status': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'gpa': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'group': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.Group']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        },
        u'rush_forms.form': {
            'Meta': {'object_name': 'Form'},
            'button_text': ('django.db.models.fields.CharField', [], {'default': "u'Submit'", 'max_length': '50'}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'email_copies': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'email_from': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'email_message': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'email_subject': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'response': ('django.db.models.fields.TextField', [], {}),
            'send_email': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'}),
            'status': ('model_utils.fields.StatusField', [], {'default': "u'draft'", 'max_length': '100', u'no_check_for_status': 'True'}),
            'status_changed': ('model_utils.fields.MonitorField', [], {'default': 'datetime.datetime.now', u'monitor': "u'status'"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        },
        u'universities.university': {
            'Meta': {'object_name': 'University'},
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.Group']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        }
    }

    complete_apps = ['chapters']