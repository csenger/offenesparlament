OffenesParlament
================

OffenesParlament ist eine Webplatform, welche die Arbeit des Bundestags und
Bundesrats transparent und nachvollziehbar machen soll. Der Schwerpunkt liegt 
dabei auf den laufenden Arbeitsprozessen des Parlaments - nicht auf dem
Abstimmungsverhalten einzelner Abgeordneter oder dem Inhalt der Dokumente.

Dieses README befasst sich nur mit den technischen Aspekten der Seite, für 
weitere inhaltliche Informationen besuchen Sie: http://offenesparlament.de.


Extract, Transform, Load
------------------------

Die Inhalte der Seite entstammen im wesentlichen zwei Systemen:

* Dem CMS des Bundestags (Profile von Abgeordneten, Ausschüssen und
  Nachrichten)
* Das Dokumenten- und Informationsportal des Bundestags und Bundesrats für
  aktuelle Vorgänge, Links und Beteiligte.

Die Auswertung der Inhalte erfolgt in den folgenden Schritten:

* Extraktion (``offenesparlament.extract``): die Webseiten werden gescraped
  und in einer Instanz der Webstore abgelegt. 
* Transformation (``offenesparlament.transform``): Inhalte werden
  angereichert, Personendaten vereinheitlicht und Texte analysiert.
* Load (``offenesparlament.load``): Daten aus dem Webstore-System werden in
  die eigentliche produktiv-Datenbank geladen.


Feature-Ideen
-------------

* Ablauf-Titel automatisch kürzen.
* WebTV des Bundestags scrapen.


Installation
------------

Erzeuge eine virtualenv, clone offenesparlament und installiere es::

  virtualenv --no-site-packages offenes_parlament
  cd offenes_parlament
  bin/pip install -e git+https://github.com/pudo/offenesparlament

Für die Suche benötigt offenesparlament eine Solrinstallation. Du
kannst Solr auf dienem Rechner installieren und konfigurieren. Für
Entwicklungs- oder Testinstallationen ist es aber am enfachsten, Solr
herunterzuladen, zu entpacken und von der Kommandozeile zu starten::

    mkdir op_solr
    cd op_solr
    wget http://ftp-stud.hs-esslingen.de/pub/Mirrors/ftp.apache.org/dist/lucene/solr/3.6.1/apache-solr-3.6.1.tgz
    tar xzf apache-solr-3.6.1.tgz
    cd apache-solr-3.6.1/example
    java -jar start.jar

Solr ist dann unter http://localhost:8983/solr erreichbar.

Konfiguration
-------------

Während der Transformation der Daten normalisiert offenesparlament die Namen der Abgeordneten. Dazu verwendet es den Nomenklatura_ webservice. Für die Konfiguration benötigst Du einen apikey. Diesen findest Du nach der Anmeldung dort in deinem Profil.

Die Standardeinstellungen für offenesparlament befinden sich in
src/offenesparlament/offenesparlament/default_settings.py. Der
Einfachheit halber verwenden wir hier sqlite statt postgres. 
Den Pfad zu dieser Datei exportieren wir als Umgebungsvariable 
PARLAMENT_SETTINGS::

  cat > einstellungen.py <<EOF
  SQLALCHEMY_DATABASE_URI = 'sqlite:///parlament.db'
  ETL_URL = 'sqlite:///parlament_etl.db'
  SOLR_URL = 'http://localhost:8983/solr'
  NOMENKLATURA_PERSONS_DATASET = 'offenesparlament'
  NOMENKLATURA_API_KEY = '<your nomenklatura api key>'
  EOF
  export PARLAMENT_SETTINGS='/pfad/zu/einstellungen.py'


Import der Daten
----------------

Es wird mehrere Stunden dauern, die Daten in offenes Parlament zu
importieren. Insbesondere `extract_docs` und `transform` dauern lange.

  echo $PARLAMENT_SETTINGS
  /pfad/zu/einstellungen.py

  bin/python src/offenesparlament/offenesparlament/manage.py extract_base
  bin/python src/offenesparlament/offenesparlament/manage.py extract_docs
  bin/python src/offenesparlament/offenesparlament/manage.py extract_votes
  bin/python src/offenesparlament/offenesparlament/manage.py extract_media

  bin/python src/offenesparlament/offenesparlament/manage.py transform

  bin/python src/offenesparlament/offenesparlament/manage.py load  


Starten von offenesparlament
----------------------------

  bin/python src/offenesparlament/offenesparlament/manage.py runserver


Kontakt
-------

* Friedrich Lindenberg <friedrich.lindenberg@okfn.org>
* http://lists.okfn.org/mailman/listinfo/offenes-parlament


Lizenz
------

Der Code von OffenesParlament steht unter der Affero GPL v3-Lizenz. Der Text
der Lizenz ist unter http://www.gnu.org/licenses/agpl.html einsehbar.





.. _Nomenklatura: http://nomenklatura.okfnlabs.org

psql -c "COPY (SELECT * FROM webtv_speech ws LEFT JOIN speech s ON s.wahlperiode = CAST(ws.wp AS integer) AND s.sitzung = CAST(ws.session AS integer) AND s.sequence = ws.sequence ORDER BY ws.wp, ws.session, ws.sequence) TO STDOUT WITH CSV HEADER;" parlament_etl >speeches.csv
