from flask import render_template
from flask import request
from app import app
import unicodedata
from urllib.parse import unquote

@app.route('/')
def home():
  return render_template('home.html', title='Accueil')

@app.route('/search')
def search():
  query = request.args.get('search')

  if query:
    results = []

    if len(query) == 1:
      research = 'char'
    elif query.isnumeric() :
      research = 'dec'
    elif query[0:2] == 'u+' or query[0:2] == 'U+' :
      research = 'code'
    else :
      research = 'name'

    for i in range(230000):

      if research == 'char' and (query == chr(i) or query.upper() in unicodedata.name(chr(i), 'Name Not Found')):
        results.append({
          'display': chr(i),
          'name': unicodedata.name(chr(i), 'Name Not Found'),
          'decimal': i
        })
      if research == 'dec' and query in str(i) and i not in range(55296, 57343):
        results.append({
          'display': chr(i),
          'name': unicodedata.name(chr(i), 'Name Not Found'),
          'decimal': i
        })
      if research == 'code' and (unquote(query) == 'U+%04x' % ord(chr(i)) or unquote(query) == 'u+%04x' % ord(chr(i))) and i not in range(55296, 57343):
        results.append({
          'display': chr(i),
          'name': unicodedata.name(chr(i), 'Name Not Found'),
          'decimal': i
        })
      if research == 'name' and query.upper() in unicodedata.name(chr(i), 'Name Not Found'):
        results.append({
          'display': chr(i),
          'name': unicodedata.name(chr(i), 'Name Not Found'),
          'decimal': i
        })
    
    return render_template('search.html', title='Recherche', search=True, results=results, itemsfound=len(results))

  return render_template('search.html', title='Recherche', search=True)

@app.route('/unicode/<codepoint>')
def character(codepoint):

  char = chr(int(codepoint))

  unichar = {
    'codepoint': 'U+%04x' % ord(char),
    'name': unicodedata.name(char, 'Name Not Found'),
    'html': str(char.encode('ascii', 'xmlcharrefreplace'))[2:-1],
    'decimal': int(codepoint),
    'display': char,
    'category': unicodedata.category(char)
  }

  return render_template('unicode.html', title=char, character=unichar)