#!/usr/bin/python3.6
import argparse
from datetime import datetime
import os

from dateutil.relativedelta import relativedelta
from pdfrw import PdfReader, PageMerge, PdfWriter
from PIL import Image
from reportlab.pdfgen import canvas
import yaml


class SizeSignature(Exception):
    def __init__(self, msg):
        self.message = msg
        Exception.__init__(self, msg)


def read_yaml(path_conf):
    """
    Read the configuration file.
    """
    with open(path_conf, 'r') as conf_yaml:
        conf = yaml.load(conf_yaml, Loader=yaml.SafeLoader)
    return conf


def create_date_list(date_debut_str, date_fin_str):
    """
    Create a list of date.
    """
    date_debut = datetime.strptime(date_debut_str, '%d/%m/%Y')
    date_fin = datetime.strptime(date_fin_str, '%d/%m/%Y')
    date_list = []
    date = date_debut
    while date <= date_fin:
        date_list.append(date.strftime('%d/%m'))
        date += relativedelta(days=1)
    return date_list


def get_pos_sign(image):
    """
    Return the position where to place the  signature in the PDF.
    """
    path_image = os.path.join(os.path.dirname(__file__), conf['signature'])
    im = Image.open(path_image)
    width, height = im.size
    pos_x_im = 582 - width
    pos_y_im = 132 - height
    if pos_x_im < 0 and pos_y_im < 0:
        msg = "largeur et hauteur de la signature trop grand, réduire sa taille."
        raise SizeSignature(msg)
    else:
        if pos_x_im < 0:
            msg = "largeur de la signature trop grande, réduire sa largeur."
            raise SizeSignature(msg)
        elif pos_y_im < 0:
            msg = "hauteur de la signature trop grande, réduire sa hauteur."
            raise SizeSignature(msg)
    return pos_x_im, pos_y_im


def create_overlay(motif, conf, jour, mois):
    """
    Create the data that will be overlayed on top
    of the form that we want to fill.
    """
    c = canvas.Canvas('overlay.pdf')
    pos_x_im, pos_y_im = get_pos_sign(conf['signature'])
    c.drawImage(conf['signature'], pos_x_im, pos_y_im)
    c.drawString(140, 620, conf['nom_prenom'])
    c.drawString(140, 590, conf['date_de_naissance'])
    c.drawString(140, 558, conf['adresse'])
    c.drawString(370, 140, conf['lieu'])
    c.drawString(480, 140, jour)
    c.drawString(503, 140, mois)
    c.setFont("Courier", 19)
    if motif == 'travail':
        c.drawString(48, 422, u'\u2713')
    elif motif == 'course':
        c.drawString(48, 348, u'\u2713')
    elif motif == 'santé':
        c.drawString(48, 303, u'\u2713')
    elif motif == 'famille':
        c.drawString(48, 272, u'\u2713')
    elif motif == 'sport':
        c.drawString(48, 226, u'\u2713')
    c.save()


def merge_pdfs(form_pdf, overlay_pdf, output):
    """
    Merge the specified fillable form PDF with the  overlay PDF
    and save the output.
    """
    form = PdfReader(form_pdf)
    olay = PdfReader(overlay_pdf)
    for form_page, overlay_page in zip(form.pages, olay.pages):
        merge_obj = PageMerge()
        overlay = merge_obj.add(overlay_page)[0]
        PageMerge(form_page).add(overlay).render()
    writer = PdfWriter()
    writer.write(output, form)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Remplit l \'attestation de \
                                     déplacement obligatoire. Voir le fichier \
                                     conf.yaml pour la configuration.')
    parser.add_argument('motif', help='Un parmi les motifs autorisés par le\
                        gouvernement: travail, course, santé,\
                        famille et sport.')
    args = parser.parse_args()
    motif = args.motif
    working_dir = os.path.dirname(__file__)
    path_attestations = os.path.join(working_dir, 'attestations')
    try:
        os.mkdir(path_attestations)
    except FileExistsError:
        pass
    path_conf = os.path.join(working_dir, 'conf.yaml')
    conf = read_yaml(path_conf)
    dates = create_date_list(conf['date_debut'], conf['date_fin'])
    for date in dates:
        jour, mois = date.split('/')[0], date.split('/')[1]
        rep_day = f'{jour}_{mois}'
        path_rep_day = os.path.join(path_attestations, rep_day)
        try:
            os.mkdir(path_rep_day)
        except FileExistsError:
            pass
        create_overlay(motif, conf, jour, mois)
        name_output = f'attestation_{motif}_{jour}_{mois}.pdf'
        path_attestation = os.path.join(path_rep_day, name_output)
        merge_pdfs('Attestation_de_deplacement_derogatoire.pdf', 'overlay.pdf',
                   path_attestation)