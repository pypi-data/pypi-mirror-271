#    Copyright 2020 Jonas Waeber
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

from init_client import client, world_id, user_id

if __name__ == '__main__':

    for notebook in client.world.notebooks(user_id):
        notebook = client.notebook.get(notebook['id'], 1)
        print(notebook)
        if 'notesections' in notebook:
            for note_section in notebook['notesections']:
                note_section = client.notebook.note_section.get(note_section['id'], 1)
                print(note_section)
                if 'notes' in note_section:
                    for note in note_section['notes']:
                        note = client.notebook.note_section.note.get(note['id'], 1)
                        print(note)


    print("extracted")
    notebook = client.notebook.put(
        {
            'title': 'A New Notebook',
            'world': {
                'id': world_id
            }
        }
    )
    value = client.notebook.get(notebook['id'], 1)
    print(value)

    note_section = client.notebook.note_section.put(
         {
             'title': 'A new section',
             'notebook': {
                 'id': notebook['id']
             }
         }
    )
    print(client.notebook.note_section.get(note_section['id'], 2))

    note = client.notebook.note_section.note.put(
         {
             'title': "A New Note",
             'content': 'Some content',
             'notesection': {
                 'id': note_section['id']
             }
         }
     )
    print(client.notebook.note_section.note.get(note['id'], 2))

    client.notebook.note_section.note.delete(note['id'])
    client.notebook.note_section.delete(note_section['id'])
    client.notebook.delete(notebook['id'])
