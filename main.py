import re
from pprint import pprint
import csv
import pandas

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
  # print(f"slf_var_: {slf_var}")

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
  # print(org)
  return org

def _get_position(list_contact):
  pos = []
  for posit_var in list_contact:
    v = str(posit_var[4: 5][0]).split(" ")
    if len(v) > 1:
      p = v[0] + " " + v[1]

    if len(v) == 1:
      p = v[0]

    # print(p)
    # new_pos = posit_var[4:5][0]

    pos.append(p)
  # print(pos)
  return pos

def _get_contacts(list_contact):
  tel = []
  email = []
  # template_tel = re.compile(r"[^\s,\.]?\+?([7|8]{1})([\s-])?(\()?(\d{3})\)?[\s-]?(\d{3})[-\s]?(\d{2})[-\S]?(\d{2})[\s,]\(?(доб.)?\s?(\d*)(\d){0,1}")
  template_tel = re.compile(r"[^\s,\.']?\+?([7|8])\s?\(?(\d{3})\)?[-\s]?(\d{3})(-)?(\d{2})-?(\d{2})\s?\(?(доб.)?(\s*)?(\d{2,})?\)?")


  for pos_var in list_contact:
    new_pos = str(pos_var[5:6][0])
    print(new_pos)
    new_new_pos = template_tel.sub('+7(\2)\3-\5-\6, \7 \9', new_pos)
    print(new_new_pos)
    tel.append(new_new_pos)

  for pos_var in list_contact:
    new_pos = pos_var[6:7][0]

    email.append(new_pos)
  # print(pos)
  return [tel, email]

def get_dictionary_name(list_contact):
  # print(f"0:_ {_get_name(list_contact)}")
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






if __name__ == ('__main__'):
  with open('file/phonebook_raw.csv', encoding="utf-8") as f:
    r_file = csv.reader(f, delimiter=",")
    list_contact = list(r_file)[1:]
    # print(len(list_contact))
    # pprint(list_contact)
    # pprint((list_contact[0])[0:3])
    # t = str((list_contact[1][:3]))


  print("________________________________")
  contact_book = get_dictionary_name(list_contact)
  # pprint(f"{contact_book}")

  book = pandas.DataFrame(contact_book)[['lastname', 'firstname', 'surname', 'organization', 'position', 'phone']]
  print(book)
  book.to_csv('file/book.csv')

    # print(f"000: {list_contact[0]}")

# "((\+7|7|8)?(\s*|-)*(\(\d{1,}\)*|\d*)\s*(\d*)[-\s]*(\d*)*[-\s*]*(\d*)*)[-\s]*[\(*\s|\(*,\s]\({,1}(\w{,3}\.{,1})\s*(\w*)\){,1}"g
#
# "((\+7|7|8)?(\s|-)*(\(\d{1,}\)|\d*)\s*\d*[-\s]*(\d*)[-\s*]*(\d*))[-\s]*[(\(\s)|(\(,\s)]\({,1}((доб){,1}\.{,1}){,1}\s*[^,]\w*\){,1}"g
# "[^\s,]((\+7|7|8)?(\s|-)*(\(\d{1,}\)|\d*)\s*\d*[-\s]*(\d*)[-\s*]*(\d*))[-\s]*[(\(\s)|(\(,\s)]\({,1}((доб){,1}\.{,1}){,1}\s*[^,]\d*\){,1}"g
#
# "[^\s,]((\+7|7|8)?(\s|-)*(\(\d{1,}\)|\d*)\s*\d*[-\s]*(\d*)[-\s*]*(\d*))[-\s]*\(*[(,\s?)|\s?](\(*(доб){,1}\.{,1}\)*){,1}\s*[^,]\d*\){,1}[^,\s]"g
# "([^\s,\.][\+7|\s8]*[\s-]*)?\(*(\d{3,})\)?[-\s]*(\d*)[\s-]+(\d*)[\s-](\d{,3}[^,])(\({0,1}(доб)?\.\s(\d+)\){,1}){,1}[^,\s]"g