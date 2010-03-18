#!/usr/bin/env python
#   simple_password_generator.py - generate password from key and your account
#   Copyright (C) 2009,2010  bhuztez <bhuztez@gmail.com>
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Affero General Public License as
#   published by the Free Software Foundation, either version 3 of the
#   License, or (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU Affero General Public License for more details.
#
#   You should have received a copy of the GNU Affero General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.

from base64 import b64encode
from binascii import b2a_hex, b2a_hqx
import hashlib
from hmac import new
import sys
from time import strftime

import gobject
import gtk


UI = '''
<?xml version="1.0"?>
<interface>
  <requires lib="gtk+" version="2.16"/>
  <!-- interface-naming-policy toplevel-contextual -->
  <object class="GtkWindow" id="window">
    <signal name="destroy" handler="on_window_destroy"/>
    <child>
      <object class="GtkVBox" id="vbox1">
        <property name="visible">True</property>
        <child>
          <object class="GtkTable" id="table1">
            <property name="visible">True</property>
            <property name="n_rows">5</property>
            <property name="n_columns">2</property>
            <property name="column_spacing">10</property>
            <property name="row_spacing">10</property>
            <child>
              <object class="GtkComboBox" id="digest">
                <property name="visible">True</property>
                <property name="model">liststore2</property>
                <property name="active">7</property>
                <signal name="changed" handler="on_changed"/>
                <child>
                  <object class="GtkCellRendererText" id="cellrenderertext2"/>
                  <attributes>
                    <attribute name="text">0</attribute>
                  </attributes>
                </child>
              </object>
              <packing>
                <property name="left_attach">1</property>
                <property name="right_attach">2</property>
                <property name="top_attach">3</property>
                <property name="bottom_attach">4</property>
                <property name="x_padding">10</property>
              </packing>
            </child>
            <child>
              <object class="GtkComboBox" id="strength">
                <property name="visible">True</property>
                <property name="model">liststore1</property>
                <property name="active">1</property>
                <signal name="changed" handler="on_changed"/>
                <child>
                  <object class="GtkCellRendererText" id="cellrenderertext1"/>
                  <attributes>
                    <attribute name="text">0</attribute>
                  </attributes>
                </child>
              </object>
              <packing>
                <property name="left_attach">1</property>
                <property name="right_attach">2</property>
                <property name="top_attach">2</property>
                <property name="bottom_attach">3</property>
                <property name="x_padding">10</property>
              </packing>
            </child>
            <child>
              <object class="GtkEntry" id="key">
                <property name="visible">True</property>
                <property name="can_focus">True</property>
                <signal name="changed" handler="on_changed"/>
                <signal name="move_cursor" handler="on_changed"/>
              </object>
              <packing>
                <property name="left_attach">1</property>
                <property name="right_attach">2</property>
                <property name="top_attach">1</property>
                <property name="bottom_attach">2</property>
                <property name="x_padding">10</property>
              </packing>
            </child>
            <child>
              <object class="GtkEntry" id="account">
                <property name="visible">True</property>
                <property name="can_focus">True</property>
                <signal name="changed" handler="on_changed"/>
                <signal name="move_cursor" handler="on_changed"/>
              </object>
              <packing>
                <property name="left_attach">1</property>
                <property name="right_attach">2</property>
                <property name="x_padding">10</property>
              </packing>
            </child>
            <child>
              <object class="GtkLabel" id="label5">
                <property name="visible">True</property>
                <property name="label" translatable="yes">length</property>
              </object>
              <packing>
                <property name="top_attach">4</property>
                <property name="bottom_attach">5</property>
                <property name="x_options"></property>
                <property name="x_padding">10</property>
              </packing>
            </child>
            <child>
              <object class="GtkLabel" id="label4">
                <property name="visible">True</property>
                <property name="label" translatable="yes">digest</property>
              </object>
              <packing>
                <property name="top_attach">3</property>
                <property name="bottom_attach">4</property>
                <property name="x_options"></property>
                <property name="x_padding">10</property>
              </packing>
            </child>
            <child>
              <object class="GtkLabel" id="label3">
                <property name="visible">True</property>
                <property name="label" translatable="yes">strength</property>
              </object>
              <packing>
                <property name="top_attach">2</property>
                <property name="bottom_attach">3</property>
                <property name="x_options"></property>
                <property name="x_padding">10</property>
              </packing>
            </child>
            <child>
              <object class="GtkLabel" id="label2">
                <property name="visible">True</property>
                <property name="label" translatable="yes">key</property>
              </object>
              <packing>
                <property name="top_attach">1</property>
                <property name="bottom_attach">2</property>
                <property name="x_options"></property>
                <property name="x_padding">10</property>
              </packing>
            </child>
            <child>
              <object class="GtkLabel" id="label1">
                <property name="visible">True</property>
                <property name="label" translatable="yes">account</property>
              </object>
              <packing>
                <property name="x_options"></property>
                <property name="x_padding">10</property>
              </packing>
            </child>
            <child>
              <object class="GtkSpinButton" id="length">
                <property name="visible">True</property>
                <property name="can_focus">True</property>
                <property name="adjustment">lengthadjustment</property>
                <signal name="changed" handler="on_changed"/>
              </object>
              <packing>
                <property name="left_attach">1</property>
                <property name="right_attach">2</property>
                <property name="top_attach">4</property>
                <property name="bottom_attach">5</property>
                <property name="x_padding">10</property>
              </packing>
            </child>
          </object>
          <packing>
            <property name="expand">False</property>
            <property name="fill">False</property>
            <property name="padding">10</property>
            <property name="position">0</property>
          </packing>
        </child>
        <child>
          <object class="GtkTextView" id="result">
            <property name="width_request">400</property>
            <property name="height_request">100</property>
            <property name="visible">True</property>
            <property name="can_focus">True</property>
            <property name="editable">False</property>
            <property name="wrap_mode">word</property>
            <property name="left_margin">10</property>
            <property name="right_margin">10</property>
            <property name="buffer">resulttextbuffer</property>
          </object>
          <packing>
            <property name="position">1</property>
          </packing>
        </child>
      </object>
    </child>
  </object>
  <object class="GtkAdjustment" id="lengthadjustment">
    <property name="value">16</property>
    <property name="lower">8</property>
    <property name="upper">32</property>
    <property name="step_increment">2</property>
    <property name="page_increment">8</property>
  </object>
  <object class="GtkListStore" id="liststore1">
    <columns>
      <!-- column-name item -->
      <column type="gchararray"/>
    </columns>
    <data>
      <row>
        <col id="0" translatable="yes">very weak</col>
      </row>
      <row>
        <col id="0" translatable="yes">weak</col>
      </row>
      <row>
        <col id="0" translatable="yes">normal</col>
      </row>
    </data>
  </object>
  <object class="GtkListStore" id="liststore2">
    <columns>
      <!-- column-name item -->
      <column type="gchararray"/>
    </columns>
    <data>
      <row>
        <col id="0" translatable="yes">dss1</col>
      </row>
      <row>
        <col id="0" translatable="yes">md2</col>
      </row>
      <row>
        <col id="0" translatable="yes">md4</col>
      </row>
      <row>
        <col id="0" translatable="yes">md5</col>
      </row>
      <row>
        <col id="0" translatable="yes">ripemd160</col>
      </row>
      <row>
        <col id="0" translatable="yes">sha1</col>
      </row>
      <row>
        <col id="0" translatable="yes">sha224</col>
      </row>
      <row>
        <col id="0" translatable="yes">sha256</col>
      </row>
      <row>
        <col id="0" translatable="yes">sha384</col>
      </row>
      <row>
        <col id="0" translatable="yes">sha512</col>
      </row>
    </data>
  </object>
  <object class="GtkTextBuffer" id="resulttextbuffer"/>
</interface>
'''

class window:
    def get(self, name):
        return self.builder.get_object(name)

    def __init__(self):
        self.builder = gtk.Builder()
        self.builder.add_from_string(UI)
        
        self.get("lengthadjustment").set_value(16)
        self.get("window").show_all()
        self.builder.connect_signals(self)

        self.clipboard = gtk.Clipboard()
        self.tag = None

        self.text_buffer = self.get("resulttextbuffer")
        self.text_buffer.create_tag('em', foreground='purple')
        self.text_buffer.create_tag('error', foreground='red')
        self.text_buffer.create_tag('time', foreground='gray')
        self.text_buffer.create_tag('param', foreground='blue')
        gtk.main()

    def on_window_destroy(self, window):
        # FIXME: conflicts with CLIPMAN under Xfce
        self.clipboard.store()
        gtk.main_quit()

    def reset_timer(self):
        if self.tag:
            gobject.source_remove(self.tag)
        self.tag = gobject.timeout_add(500, self.on_timeout)

    def on_changed(self, widget, *args):
        self.reset_timer()

    def get_input(self):
        return (
            self.get("account").get_text(),
            self.get("key").get_text(),
            self.get("strength").get_active_text(),
            self.get("digest").get_active_text(),
            self.get("length").get_value_as_int())

    def generate_password(self, account, key, encode, digestmod):
        encoder = {
          "very weak": b2a_hex,
          "weak"     : b64encode,
          "normal"   : b2a_hqx,
        }

        
        hmac = new(key, account, lambda: hashlib.new(digestmod))
        encode = encoder[encode]
        return encode(hmac.digest())

    def truncate_password(self, password, length):
        if len(password) < length:
            raise Exception("%s is too long for current settings"%(length))
        else:
            start = (len(password)-length)/2
            return password[start:start+length]

    def on_timeout(self):
        # calculate
        (account, key, strength, digest, length) = self.get_input()
        text_buffer = self.text_buffer
        
        iterator = text_buffer.get_end_iter()

        if account == "" or key == "":
            password = ""
        else:
            password = self.generate_password(account, key, strength, digest)
            text_buffer.insert_with_tags_by_name(iterator, strftime("%H:%M:%S "), "time")

            try:
                password = self.truncate_password(password, length)
                text_buffer.insert_with_tags_by_name(iterator, account, "em")
                text_buffer.insert(iterator, " (strength=")
                text_buffer.insert_with_tags_by_name(iterator, strength, "param")
                text_buffer.insert(iterator, ", digest=")
                text_buffer.insert_with_tags_by_name(iterator, digest, "param")
                text_buffer.insert(iterator, ", length=")
                text_buffer.insert_with_tags_by_name(iterator, str(length), "param")
                text_buffer.insert(iterator, ")\n")
                
                # FIXME: conflicts with CLIPMAN under Xfce
                self.clipboard.set_text(password)
            except Exception, err:
                text_buffer.insert_with_tags_by_name(iterator, "error:", "error")
                text_buffer.insert(iterator, " %s\n"%(err))

            self.get("result").scroll_to_iter(iterator, 0.0)

        return False

if __name__ == '__main__':
    window()


