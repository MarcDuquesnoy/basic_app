import streamlit as st
import psycopg2
import pandas as pd

db_connection = psycopg2.connect(dbname='postgres', user='postgres', password='allezlesverts', host='localhost',
                                     port=5432)

def selector():

    col1, col2 = st.columns(2)

    with col1:
        date = st.date_input("Date de la séance", value=None)

    with col2:
        stretch = st.radio("Séance d'étirements", [1, 0])

    col1, col2 = st.columns(2)

    with col1:
        exercices = st.slider("Nombre d'exercices", 1, 10)

    with col2:
        series = st.slider("Nombre de series", 1, 10)

    return date, exercices, stretch, series


def list_body():

    db_cursor = db_connection.cursor()
    db_cursor.execute("""select b.reference_exercice from basic.body b """)
    x = db_cursor.fetchall()
    return tuple([i[0] for i in x])


def import_training(date, exercices, stretch):

    db_cursor = db_connection.cursor()
    db_cursor.execute("""insert into basic.trainings("date", exercices_nb, stretching) VALUES('""" + str(date) +
                      """', """ + str(exercices) + """, """ + str(stretch) + """);""")

    st.markdown("""insert into basic.trainings("date", exercices_nb, stretching) VALUES('""" + str(date) +
                      """', """ + str(exercices) + """, """ + str(stretch) + """);""")
    db_connection.commit()


def import_series(series):

    db_cursor = db_connection.cursor()
    db_cursor.execute("""select t.training_id from basic.trainings t ORDER by training_id desc limit 1""")
    id = db_cursor.fetchall()[0][0]

    for i in range(1, series + 1):

        exercice = st.session_state['A' + str(i)]
        db_cursor.execute("""select b.body_id from basic.body b where b.reference_exercice = '""" + str(exercice) + """'""")
        id_body = db_cursor.fetchall()[0][0]

        series = st.session_state['B' + str(i)]
        weight = st.session_state['C' + str(i)]
        comment = st.session_state['D' + str(i)]
        repetition = st.session_state['E' + str(i)]

        db_cursor.execute("""insert into basic.exercices (training_id, body_id, series, weight, repetition, comment) values ("""
                          + str(id) + """, """
                          + str(id_body) + """, """
                          + str(series) + """, """
                          + str(weight) + """, """
                          + str(repetition) + """, '"""
                          + str(comment) + """');""")
        db_connection.commit()


def basic_results():

    db_cursor = db_connection.cursor()
    db_cursor.execute("""select count(*) from basic.trainings t""")
    training_nb = db_cursor.fetchall()[0][0]

    db_cursor = db_connection.cursor()
    db_cursor.execute("""select count(*), to_char(date, 'IYYY-IW') from basic.trainings t
                      group by to_char(date, 'IYYY-IW')""")
    training = pd.DataFrame(db_cursor.fetchall(), columns=["count", "date"])

    db_cursor = db_connection.cursor()
    db_cursor.execute("""(select 
        b.reference_body, count(*), 'Partie du corps' from basic.exercices e 
    left join 
        basic.body b 
    on 
        e.body_id = b.body_id 
    group by 
        b.reference_body
    order by 
        count(*)
    desc)
    
    union all
    
    (select 
        b.reference_exercice, count(*), 'Exercice' from basic.exercices e 
    left join
        basic.body b 
    on 
        e.body_id = b.body_id 
    group by 
        b.reference_exercice
    order by 
        count(*)
    desc)""")
    best_exercices = pd.DataFrame(db_cursor.fetchall(), columns=["reference", "count", "id"])

    db_cursor = db_connection.cursor()
    db_cursor.execute("""select max(e.weight) from basic.exercices e""")
    best_weight = db_cursor.fetchall()[0][0]

    st.write(f"### Nombre de séances : :red[{training_nb}]")
    st.write(f"### Plus grosse poussée : :red[{best_weight}] Kg.")
