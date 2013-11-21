# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Chapter'
        db.create_table(u'chapters_chapter', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now)),
            ('modified', self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now)),
            ('status', self.gf('model_utils.fields.StatusField')(default='excellence', max_length=100, no_check_for_status=True)),
            ('status_changed', self.gf('model_utils.fields.MonitorField')(default=datetime.datetime.now, monitor=u'status')),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('slug', self.gf('django.db.models.fields.CharField')(max_length=2000, null=True, blank=True)),
            ('fraternity', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['fraternities.Fraternity'], null=True, blank=True)),
            ('university', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['universities.University'], null=True, blank=True)),
            ('fraternity_title', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('university_title', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('description', self.gf('model_utils.fields.SplitField')(no_excerpt_field=True, blank=True)),
            ('location', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('awards', self.gf('model_utils.fields.SplitField')(no_excerpt_field=True, blank=True)),
            ('philanthropy', self.gf('model_utils.fields.SplitField')(no_excerpt_field=True, blank=True)),
            ('potential_new_members', self.gf('model_utils.fields.SplitField')(no_excerpt_field=True, blank=True)),
            ('facebook', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('fb_status', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('cost', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('gpa', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('linked_group', self.gf('django.db.models.fields.related.OneToOneField')(blank=True, related_name='linked_chapter', unique=True, null=True, to=orm['auth.Group'])),
            ('linked_rush_group', self.gf('django.db.models.fields.related.OneToOneField')(blank=True, related_name='linked_chapter_rush', unique=True, null=True, to=orm['auth.Group'])),
            ('linked_pending_group', self.gf('django.db.models.fields.related.OneToOneField')(blank=True, related_name='linked_chapter_pending', unique=True, null=True, to=orm['auth.Group'])),
            (u'_philanthropy_excerpt', self.gf('django.db.models.fields.TextField')()),
            (u'_description_excerpt', self.gf('django.db.models.fields.TextField')()),
            (u'_awards_excerpt', self.gf('django.db.models.fields.TextField')()),
            (u'_potential_new_members_excerpt', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'chapters', ['Chapter'])

        # Adding M2M table for field groups on 'Chapter'
        m2m_table_name = db.shorten_name(u'chapters_chapter_groups')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('chapter', models.ForeignKey(orm[u'chapters.chapter'], null=False)),
            ('group', models.ForeignKey(orm[u'auth.group'], null=False))
        ))
        db.create_unique(m2m_table_name, ['chapter_id', 'group_id'])

        # Adding model 'Position'
        db.create_table(u'chapters_position', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now)),
            ('modified', self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('slug', self.gf('django.db.models.fields.CharField')(max_length=2000, null=True, blank=True)),
            ('chapter', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['chapters.Chapter'])),
        ))
        db.send_create_signal(u'chapters', ['Position'])


    def backwards(self, orm):
        # Deleting model 'Chapter'
        db.delete_table(u'chapters_chapter')

        # Removing M2M table for field groups on 'Chapter'
        db.delete_table(db.shorten_name(u'chapters_chapter_groups'))

        # Deleting model 'Position'
        db.delete_table(u'chapters_position')


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
            'linked_group': ('django.db.models.fields.related.OneToOneField', [], {'blank': 'True', 'related_name': "'linked_chapter'", 'unique': 'True', 'null': 'True', 'to': u"orm['auth.Group']"}),
            'linked_pending_group': ('django.db.models.fields.related.OneToOneField', [], {'blank': 'True', 'related_name': "'linked_chapter_pending'", 'unique': 'True', 'null': 'True', 'to': u"orm['auth.Group']"}),
            'linked_rush_group': ('django.db.models.fields.related.OneToOneField', [], {'blank': 'True', 'related_name': "'linked_chapter_rush'", 'unique': 'True', 'null': 'True', 'to': u"orm['auth.Group']"}),
            'location': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'philanthropy': ('model_utils.fields.SplitField', [], {u'no_excerpt_field': 'True', 'blank': 'True'}),
            'potential_new_members': ('model_utils.fields.SplitField', [], {u'no_excerpt_field': 'True', 'blank': 'True'}),
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
            'description': ('model_utils.fields.SplitField', [], {u'no_excerpt_field': 'True'}),
            'facebook': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'fb_status': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'gpa': ('django.db.models.fields.FloatField', [], {}),
            'group': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.Group']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'}),
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