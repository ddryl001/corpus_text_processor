#!/usr/local/bin/python3
# DESCRIPTION: Given a file or files passed as arguments to the script,
# find-replace the listed characters.


import chardet
import codecs
from parsers import encoding
import os
import re
import shutil
import string
import sys


def run(original_file, source, destination, file_name, extension, values):
    if extension not in ['.html', '.txt', '.xml']:
        return {'name': file_name, 'result': False, 'message': 'Not a .txt file'}
    rawdata = open(original_file, 'rb').read()
    detected = chardet.detect(rawdata)
    encoding_method = encoding.get_encoding(detected['encoding'])
    if not encoding_method:
        encoding_method = 'utf8'
    with codecs.open(original_file, 'r', encoding=encoding_method) as f:
        try:
            filepath = os.path.dirname(original_file)
            relative_directory = os.path.relpath(filepath, source)
            output_directory = os.path.join(destination, relative_directory)
            output_filename = os.path.join(output_directory, file_name)
            if not os.path.exists(output_directory):
                os.makedirs(output_directory)
            # create a new file with that name, "w" is for writable
            output_file = open(output_filename, "w")
            # for each line in this file
            for line in f:
                # replace tabs with <tab>
                line = re.sub(r'\t', '<tab>', line)
                # replace smart quotes with regular quotes
                line = line.replace(u'\u2018', u"'")
                line = line.replace(u'\u2019', u"'")
                line = line.replace(u'\u201a', u"'")
                line = line.replace(u'\u201b', u"'")
                line = line.replace(u'\u201c', u'"')
                line = line.replace(u'\u201d', u'"')
                line = line.replace(u'\u201e', u'"')
                line = line.replace(u'\u201f', u'"')
                line = line.replace(u'\u2032', u"'")
                line = line.replace(u'\u2035', u"'")
                line = line.replace(u'\u2033', u'"')
                line = line.replace(u'\u2034', u'"')
                line = line.replace(u'\u2036', u'"')
                line = line.replace(u'\u2037', u'"')
                # replace i with diacritics with quotes
                line = line.replace('ì', u'"')
                line = line.replace('í', u'"')
                # replace ellipsis with single period
                line = line.replace(u'\u2024', u'.')
                line = line.replace(u'\u2025', u'.')
                line = line.replace(u'\u2026', u'.')
                # replace Armenian apostophre with regular apostophre
                line = line.replace(u'\u055a', u"'")
                # replace inverted question mark with nothing
                line = line.replace(u'\u00bf', u' ')
                # replace all dashes with regular hifen
                line = line.replace(u'\u2010', u'-')
                line = line.replace(u'\u2011', u'-')
                line = line.replace(u'\u2012', u'-')
                line = line.replace(u'\u2013', u'-')
                line = line.replace(u'\u2014', u'-')
                line = line.replace(u'\u2015', u'-')
                # sentence normalization
                line = re.sub(r'([\.\?;:])([A-Z][a-z]+)', '\g<1> \g<2>', line)
                line = re.sub(r'([,;:])([a-z][a-z]+)', '\g<1> \g<2>', line)
                line = re.sub(r'([a-z])([A-Z])', '\g<1> \g<2>', line)
                line = re.sub(r'([\.\?;:])([0-9]+\s+)', '\g<1> \g<2>', line)
                # line = re.sub(r'\r',' ', line)
                line = re.sub(r'([a-z])(\n[A-Z])', '\g<1>. \g<2>', line)
                # flatten diacritics
                line = re.sub(r'[áàãäâåāăąǎȃȧ]', 'a', line)
                line = re.sub(r'[ÁÀÃÄÂÅĀĂĄǍȂȦ]', 'A', line)
                line = re.sub(r'[éèêëēĕėęěȇ]', 'e', line)
                line = re.sub(r'[ÉÈÊËĒĔĖĘĚȆ]', 'E', line)
                line = re.sub(r'[íìîïīĭįǐȋ]', 'i', line)
                line = re.sub(r'[ÍÌÎÏĪĬĮİǏȊ]', 'I', line)
                line = re.sub(r'[øóòöõôȏȯ]', 'o', line)
                line = re.sub(r'[ØÓÒÖÕÔȎȮ]', 'O', line)
                line = re.sub(r'[úùüûǔȗ]', 'u', line)
                line = re.sub(r'[ÚÙÜÛǓȖ]', 'U', line)
                line = re.sub(r'[ÝȲ]', 'Y', line)
                line = re.sub(r'[ýÿȳ]', 'y', line)
                line = re.sub(r'œ', 'oe', line)
                line = re.sub(r'æ', 'ae', line)
                line = re.sub(r'Æ', 'AE', line)
                line = re.sub(r'[çćĉċč]', 'c', line)
                line = re.sub(r'[ÇĆĈĊČ]', 'C', line)
                line = re.sub(r'ñ', 'n', line)
                line = re.sub(r'Ñ', 'N', line)
                if values['removeNonEnglish'] is not False:
                    # use a regular expression to find non-english characters and
                    # replace them with space
                    # capture any name that is written in different scripts
                    line = re.sub(r'[^\x00-\x7F]+', ' ', line)
                # get rid of weird line breaks (this does not seem to be working)
                line = re.sub(r'([a-z]+)\s*\n\s*([a-z]+)', '\g<1> \g<2>', line)
                # get rid of all double spaces
                line = re.sub(r'\s+', ' ', line)
                #print(line)
                # get rid space in the beginning of a line
                line = line.strip()
                # re-add tab
                line = re.sub(r'<tab>', '\t', line)
                # write our text in the file
                output_file.write(line + "\r\n")
                #print(line, file=output_file)
            # be polite and close the file
            output_file.close()
            return {'name': file_name, 'result': True, 'message': 'Successfully standardized.'}
        except:
            message = str(sys.exc_info()[1])
            return {'name': file_name, 'result': False, 'message': message}
