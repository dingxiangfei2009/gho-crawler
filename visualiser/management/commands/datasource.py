import time, os, csv, re, string, random
from io import StringIO
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pyvirtualdisplay import Display

from django.core.management.base import BaseCommand
from visualiser.models import Country, StatisticItem, Statistics


class Command(BaseCommand):
    help = 'Polling data from GHO data repository, with help of ' \
           'Selenium and Google Chrome WebDriver. '

    def handle(self, *args, **options):
        command_location = os.path.dirname(os.path.realpath(__file__))
        display = Display(visible=0, size=(800, 600))
        display.start()

        opts = Options()
        opts.binary_location = '/usr/bin/google-chrome-unstable'
        opts.add_experimental_option('prefs', {
            'download.default_directory': '/tmp'
        })

        driver = webdriver.Chrome(
            os.path.join(command_location, './chromedriver'),
            chrome_options=opts)
        driver.get('http://gamapserver.who.int/gareports/Default.aspx?ReportNo=2')
        driver.execute_script('!function(){'
                              'var script=document.createElement("script");'
                              'script.src="//code.jquery.com/jquery-2.2.0.min.js";'
                              'document.body.appendChild(script);}()')
        data_tag = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(25))
        time.sleep(10)

        driver.execute_script(
            '!function(){'
              '$.ajax({'
                'url:'
                    'ClientToolbarctl_ReportViewer_ctl01.m_exportUrlBase'
                    '+"CSV"'
              '}).success(function(data){'
                  'var text=document.createElement("textarea");'
                  'text.id="%s";'
                  'text.value=data;'
                  'document.body.appendChild(text);'
              '})'
            '}();' % data_tag)
        time.sleep(10)
        data = driver.find_element_by_id(data_tag).get_attribute('value')

        file = StringIO(data)
        rows = []
        for row in csv.reader(file):
            rows.append(row)
        file.close()

        driver.quit()
        display.stop()

        rows[-1:] = []
        rows[2:3] = []
        rows[0:1] = []    # remove the first row, nothing
        print(rows[0][0])
        print(rows[0][1])
        year = re.match(r'Year\s*(\d{4})', rows[0][0]).group(1)
        week = re.match(r'Week\s*(\d+)', rows[0][1]).group(1)
        end_of_week = re.sub(
                r'.+to (\d{2})/(\d{2})/(\d{4}).+',
                r'\3-\2-\1',
                rows[0][2])
        print('End of week ', end_of_week)
        serial = '%s-%s' % (year, week)
        print('Serial', serial)
        for row in rows[2:]:  # skip the first row
            country = row[0]
            influenza_a = row[8]
            influenza_b = row[12]
            influenza_total = row[13]
            activity = row[14]

            print("%s %s %s %s %s" % (country, influenza_a, influenza_b, influenza_total, activity))

            country_query = Country.objects.filter(name=country)
            if country_query.exists():
                country_obj = country_query[0]
            else:
                country_obj = Country.objects.create(name=country, description=country)
            statistics_influenza_a = StatisticItem.objects.filter(name='influenza a')[0]
            statistics_influenza_b = StatisticItem.objects.filter(name='influenza b')[0]
            statistics_influenza_total = StatisticItem.objects.filter(name='influenza all')[0]
            statistics_activity = StatisticItem.objects.filter(name='influenza activity')[0]

            Statistics.objects.create(
                country=country_obj,
                name=statistics_influenza_a,
                int_value=influenza_a,
                date=end_of_week,
                serial=serial)
            Statistics.objects.create(
                country=country_obj,
                name=statistics_influenza_b,
                int_value=influenza_b,
                date=end_of_week,
                serial=serial)
            Statistics.objects.create(
                country=country_obj,
                name=statistics_influenza_total,
                int_value=influenza_total,
                date=end_of_week,
                serial=serial)
            Statistics.objects.create(
                country=country_obj,
                name=statistics_activity,
                string_value=activity,
                date=end_of_week,
                serial=serial)
