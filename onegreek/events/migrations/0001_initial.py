# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Event'
        db.create_table(u'events_event', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now)),
            ('modified', self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now)),
            ('start', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('end', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('status', self.gf('model_utils.fields.StatusField')(default='rush', max_length=100, no_check_for_status=True)),
            ('status_changed', self.gf('model_utils.fields.MonitorField')(default=datetime.datetime.now, monitor=u'status')),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('slug', self.gf('django.db.models.fields.CharField')(max_length=2000, null=True, blank=True)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='events', null=True, to=orm['users.User'])),
            ('description', self.gf('model_utils.fields.SplitField')(no_excerpt_field=True)),
            ('all_day', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('enable_comments', self.gf('django.db.models.fields.BooleanField')(default=True)),
            (u'_description_excerpt', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'events', ['Event'])

        # Adding model 'Attendees'
        db.create_table(u'events_attendees', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['events.Event'])),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'events', ['Attendees'])

        # Adding M2M table for field rsvps on 'Attendees'
        m2m_table_name = db.shorten_name(u'events_attendees_rsvps')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('attendees', models.ForeignKey(orm[u'events.attendees'], null=False)),
            ('user', models.ForeignKey(orm[u'users.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['attendees_id', 'user_id'])

        # Adding M2M table for field rsvps_copy on 'Attendees'
        m2m_table_name = db.shorten_name(u'events_attendees_rsvps_copy')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('attendees', models.ForeignKey(orm[u'events.attendees'], null=False)),
            ('user', models.ForeignKey(orm[u'users.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['attendees_id', 'user_id'])

        # Adding M2M table for field attendees on 'Attendees'
        m2m_table_name = db.shorten_name(u'events_attendees_attendees')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('attendees', models.ForeignKey(orm[u'events.attendees'], null=False)),
            ('user', models.ForeignKey(orm[u'users.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['attendees_id', 'user_id'])


    def backwards(self, orm):
        # Deleting model 'Event'
        db.delete_table(u'events_event')

        # Deleting model 'Attendees'
        db.delete_table(u'events_attendees')

        # Removing M2M table for field rsvps on 'Attendees'
        db.delete_table(db.shorten_name(u'events_attendees_rsvps'))

        # Removing M2M table for field rsvps_copy on 'Attendees'
        db.delete_table(db.shorten_name(u'events_attendees_rsvps_copy'))

        # Removing M2M table for field attendees on 'Attendees'
        db.delete_table(db.shorten_name(u'events_attendees_attendees'))


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
            'cost': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'description': ('model_utils.fields.SplitField', [], {u'no_excerpt_field': 'True', 'blank': 'True'}),
            'facebook': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'fb_status': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
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
        u'events.attendees': {
            'Meta': {'object_name': 'Attendees'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'attendees': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'attending'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['users.User']"}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['events.Event']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rsvps': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'rsvps'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['users.User']"}),
            'rsvps_copy': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'rsvps_copy'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['users.User']"})
        },
        u'events.event': {
            'Meta': {'object_name': 'Event'},
            u'_description_excerpt': ('django.db.models.fields.TextField', [], {}),
            'all_day': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'description': ('model_utils.fields.SplitField', [], {u'no_excerpt_field': 'True'}),
            'enable_comments': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'end': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'events'", 'null': 'True', 'to': u"orm['users.User']"}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'}),
            'start': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'status': ('model_utils.fields.StatusField', [], {'default': "'rush'", 'max_length': '100', u'no_check_for_status': 'True'}),
            'status_changed': ('model_utils.fields.MonitorField', [], {'default': 'datetime.datetime.now', u'monitor': "u'status'"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500'})
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
        },
        u'users.user': {
            'Meta': {'object_name': 'User'},
            'chapter': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['chapters.Chapter']", 'null': 'True', 'blank': 'True'}),
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'fraternity': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['fraternities.Fraternity']", 'null': 'True', 'blank': 'True'}),
            'gpa': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            'highschool_gpa': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'hometown': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'major': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'position': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['chapters.Position']", 'null': 'True', 'blank': 'True'}),
            'profile_img_id': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'profile_img_pic': ('django.db.models.fields.URLField', [], {'max_length': '500', 'blank': 'True'}),
            'profile_img_select': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'profile_img_src': ('django.db.models.fields.URLField', [], {'max_length': '500', 'blank': 'True'}),
            'status': ('model_utils.fields.StatusField', [], {'default': "'Rushing'", 'max_length': '100', u'no_check_for_status': 'True'}),
            'status_changed': ('model_utils.fields.MonitorField', [], {'default': 'datetime.datetime.now', u'monitor': "u'status'"}),
            'university': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['universities.University']", 'null': 'True', 'blank': 'True'}),
            'university_email': ('django.db.models.fields.EmailField', [], {'max_length': '255', 'blank': 'True'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'}),
            'year': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['events']