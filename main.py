import re
from pprint import pprint
import csv
import pandas
import itertools

def _get_name(list_contact):
  template_name = re.compile(r"(\'|\"){0,1}([а-яё]{3,})(\'|\"){0,1}", re.I)
  template_name_cleaned = re.compile(r"(\w+)", re.I)

  get_list_name = []

  for list_var in list_contact:
    name_str_var = str(list_var[:3])
    new_name_var = template_name.findall(name_str_var)
    new_name_cleaned = template_name_cleaned.findall(str(new_name_var))



    get_list_name.append(new_name_cleaned)

  return get_list_name

def _saerch_lastname(slf_var):

  template_lastname = re.compile(r"([а-яё]+(ич|на))", re.I)
  template_var = (template_lastname.findall(str(slf_var)))

  if template_var != []:
    # print(f"template_var:_ {template_var[-1][0] + template_var[-1][1]}")
    lastname_var = template_var[-1][0] + template_var[-1][1]
    # print(f"lastname_var:_ {lastname_var}")
    return lastname_var

def _get_organisation(list_contact):
  org = []
  for org_var in list_contact:
    new_org = org_var[3:4][0]

    org.append(new_org)

  return org

def _get_position(list_contact):
  pos = []

  for posit_var in list_contact:
    v = str(posit_var[4: 5][0])
    p = None

    if len(v) > 1:
      p = v

    elif len(v) == 1:
      p = v

    pos.append(p)

  return pos

def _get_contacts(list_contact):
  tel = []
  email = []
  template_tel = re.compile(r"[^\s,\.']?\+?([7|8])\s?\(?(\d{3})\)?[-\s]?(\d{3})(-)?(\d{2})-?(\d{2})\s?\(?(доб.)?(\s*)?(\d{2,})?\)?")


  for pos_var in list_contact:
    new_pos = str(pos_var[5:6][0])
    new_new_pos = template_tel.sub(r'+7(\2)\3-\5-\6, \7 \9', new_pos)
    tel.append(new_new_pos)

  for pos_var in list_contact:
    new_pos = pos_var[6:7][0]

    email.append(new_pos)

  return [tel, email]

def get_dictionary_name(list_contact):

  lastname_var = []
  firstname_var = []
  surname_var = []



  headers = ['lastname', 'firstname', 'surname', 'organization', 'position', 'phone', 'email']

  get_name_var = _get_name(list_contact)
  organisation_var = _get_organisation(list_contact)
  position_var = _get_position(list_contact)
  tel_var = (_get_contacts(list_contact))[0]
  email_var = (_get_contacts(list_contact))[1]

  for man_var in get_name_var:
    s = _saerch_lastname(man_var)
    # print(s)
    lastname_var.append(s)
    firstname_var.append(man_var[1])
    surname_var.append(man_var[0])

  lists = {headers[0] : lastname_var, headers[1] : firstname_var, headers[2] : surname_var,\
           headers[3] : organisation_var, headers[4] : position_var, headers[5] : tel_var,\
           headers[6] : email_var}

  return lists


def delete_dubl(book):
  i = []

  for colunm in ['lastname', 'firstname', 'surname']:
    g = (book[book[str(colunm)].duplicated() == True])

    # client's data save
    for col_name in list(g.keys())[:3]:
      for name_var in list(g[col_name]):
        if name_var != None:
          i.append(list(book[book[col_name] == name_var].index))

  unic_list = []
  for unic_var in i:
    for num_var in unic_var:
      unic_list.append(num_var)

  i = 0
  len_unic_list = len(unic_list)

  while True:
    if i == len_unic_list:
      break
    for int_var in unic_list:
      if unic_list.count(int_var) > 1:
        unic_list.remove(int_var)

    i += 1


  i = 0

  indexes_copy = []
  for index_var in range(len(unic_list)):
    if index_var / 2 % 1 == 0:

      index_1 = unic_list[index_var]
      index_2 = index_1 + 1

      index_3 = unic_list[index_var + 1]

      index_4 = index_3 + 1

      copy_str_book_first = ((book[index_1:index_1 + 1]).copy()).values[0]
      copy_str_book_two = ((book[index_3:index_3 + 1]).copy()).values[0]

      copy_str_book_keys = list(book.keys())


      i = 0
      for copy_str_first_volume in copy_str_book_first:

        copy_str_two_volume = copy_str_book_two[i]
        if copy_str_first_volume == copy_str_two_volume:
          pass

        elif copy_str_first_volume != copy_str_two_volume:

          if copy_str_first_volume == None or copy_str_first_volume == "":
            copy_str_first_volume = str(copy_str_first_volume) + " " + str(copy_str_two_volume)

            copy_str_volume = str(copy_str_first_volume).strip(" ")

          elif copy_str_two_volume == None or copy_str_two_volume == "":
            copy_str_two_volume = str(copy_str_two_volume) + " " + str(copy_str_first_volume)

            copy_str_volume = str(copy_str_two_volume).strip(" ")

          book[list(book.keys())[i]][unic_list[index_var]] = copy_str_volume
          book[list(book.keys())[i]][unic_list[index_var + 1]] = 'Delete'
          book[list(book.keys())[i]][unic_list[index_var]]

          # break
        i += 1
        if i > len(copy_str_book_two):
          print("222")
          exit()

    elif index_var / 2 % 1 != 0:
      indexes_copy.append(unic_list[index_var])

  print("__ __")

  g = (book.loc[book['phone'] != 'Delete'])
  print((g).to_csv('file/not_duble.csv'))


if __name__ == ('__main__'):
  with open('file/phonebook_raw.csv', encoding="utf-8") as f:
    r_file = csv.reader(f, delimiter=",")
    list_contact = list(r_file)[1:]



  contact_book = get_dictionary_name(list_contact)

  book = pandas.DataFrame(contact_book)[['lastname', 'firstname', 'surname', 'organization', 'position', 'phone', 'email']]

  book.to_csv('file/book.csv')

  delete_dubl(book)