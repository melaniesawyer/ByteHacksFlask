from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from dbconnect import connection
import gc

app = Flask(__name__)

Bootstrap(app) 

@app.route("/", methods = ['GET', 'POST'])
def main():
  if request.method == 'GET':
    c, conn = connection()
    c.execute("SELECT * FROM projects")
    results = c.fetchall();
    for row in results:
      print(row)
    conn.close()
    gc.collect()
    return render_template('index.html', data = results)
  if request.method == 'POST':
    return redirect(url_for('.create'))


@app.route("/create", methods = ['GET', 'POST'])
def project_form():
  if request.method == 'GET':  
    return render_template('create.html')
  
  if request.method == 'POST':
    c, conn = connection()
    org_name = request.form['org_name']
    project_name = request.form['project_name']
    description = request.form['description']
    stack = request.form['stack']
    level = request.form['level']
    tags = request.form['tags']
    email = request.form['email']
    c.execute("INSERT INTO projects (organization, project_name, project_description, stack, level, email) VALUES (%s, %s, %s, %s, %d, %d, %s", org_name, project_name, description, stack, level, email)
    conn.commit()
    conn.close()
    gc.collect()
    flash("Project Added!")
    return redirect(url_for("main"))


if __name__ == "__main__":
  app.run()
