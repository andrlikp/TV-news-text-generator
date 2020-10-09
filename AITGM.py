#!/usr/bin/env python
# coding: utf-8

# In[43]:


from PIL import Image, ImageDraw, ImageFont
from random import randrange
import random
from IPython.display import clear_output
import yaml


class Sample:

    def __init__(self, img_path, img_name):
        self.img_path = img_path
        self.img_name = img_name
        self.image = None
        self.load_image()
        self.annotationtxt = ''

    def load_image(self):
        self.image = Image.open(self.img_path).convert('RGBA')

    def annotation(self, x1, y1, text, font, enlarcoef=1):
        word = text.split()
        annotationadd = ''
        d = ImageDraw.Draw(self.image)
        for i in word:
            x2 = x1 + d.textsize(i, font)[0]
            y2 = y1 + d.textsize(i, font)[1]
            annotationadd = str(int(x1 // enlarcoef)) + ',' + str(y1) + ',' + str(int(x2 // enlarcoef)) + ',' + str(
                y1) + ',' + str(int(x1 // enlarcoef)) + ',' + str(y2) + ',' + str(int(x2 // enlarcoef)) + ',' + str(
                y2) + ',' + i + '\n'
            self.annotationtxt += annotationadd
            x1 = x2 + d.textsize(' ', font)[0]

    def annotationsave(self, path):
        # write .txt annotation file
        filename = path + "annotation_" + self.img_name + ".txt"
        with open(filename, 'w+') as file:
            file.write(self.annotationtxt)


class AITGM():
    class res():
        def __init__(self):
            self.x = None
            self.y = None

    def __init__(self, cfg_file):
        self.cfg_file = cfg_file
        self.cfg = None
        self.load_cfg()
        self.s = None
        self.checkcfgfile()
        self.res = self.res()
        self.loadvars()
        self.img_name = None

    def checkcfgfile(self):
        pass

    def loadvars(self):
        # res
        self.res.x = self.cfg['resolution']['x']
        self.res.y = self.cfg['resolution']['y']
        # live
        self.live_fnt = ImageFont.truetype(self.cfg['live']['font']['path'], self.cfg['live']['font']['size'])
        self.live_live = self.cfg['live']['live']
        self.live_recspace_x = round(self.cfg['live']['rect']['side_space_x'] * self.res.x)
        self.live_recspace_y = round(self.cfg['live']['rect']['side_space_y'] * self.res.y)
        self.live_recx = round(self.cfg['live']['rect']['x0'] * self.res.x)
        self.live_recy = round(self.cfg['live']['rect']['y0'] * self.res.y)
        self.live_recfill = self.cfg['live']['rect']['fill_live']
        self.live_reccfill = self.cfg['live']['rect']['fill_whowhere']
        self.live_tx = self.live_recx + self.live_recspace_x  # self.cfg['live']['text']['x']*self.res.x
        self.live_ty = self.live_recy + self.live_recspace_y  # self.cfg['live']['text']['y']*self.res.y
        self.live_tfill = self.cfg['live']['text']['fill']
        self.live_ttfill = self.cfg['live']['text2']['fill']
        # subtitles
        self.sub_fnt = ImageFont.truetype(self.cfg['subtitles']['font']['path'], self.cfg['subtitles']['font']['size'])
        self.sub_fnt_sz = self.cfg['subtitles']['font']['size']
        self.sub_recx = round(self.cfg['subtitles']['rect']['x0'] * self.res.x)
        self.sub_recxx = round(self.cfg['subtitles']['rect']['x1'] * self.res.x)
        self.sub_recyy = round(self.cfg['subtitles']['rect']['y1'] * self.res.y)
        self.sub_spacing_x = round(self.cfg['subtitles']['rect']['spacing_x'] * self.res.x)
        self.sub_spacing_y = round(self.cfg['subtitles']['rect']['spacing_y'] * self.res.y)
        self.sub_spacing_bl = round(self.cfg['subtitles']['rect']['spacing_bl'] * self.res.y)
        self.sub_fill = self.cfg['subtitles']['rect']['fill']
        self.sub_tfill = self.cfg['subtitles']['text']['fill']
        self.sub_lines = self.cfg['subtitles']['text']['lines']
        # source
        self.sou_fnt = ImageFont.truetype(self.cfg['source']['font']['path'], self.cfg['source']['font']['size'])
        self.sou_recxx = round(self.cfg['source']['rect']['x1'] * self.res.x)
        self.sou_recyy = round(self.cfg['source']['rect']['y1'] * self.res.y)
        self.sou_spacing_x = round(self.cfg['source']['rect']['spacing_x'] * self.res.x)
        self.sou_spacing_y = round(self.cfg['source']['rect']['spacing_y'] * self.res.y)
        self.sou_fill = self.cfg['source']['rect']['fill']
        self.sou_tfill = self.cfg['source']['text']['fill']
        # reporttitle
        self.rept_fnt = ImageFont.truetype(self.cfg['reporttitle']['font']['path'],
                                           self.cfg['reporttitle']['font']['size'])
        self.rept_fnt_sz = self.cfg['reporttitle']['font']['size']
        self.rept_recx = round(self.cfg['reporttitle']['rect']['x0'] * self.res.x)
        self.rept_recy = round(self.cfg['reporttitle']['rect']['y0'] * self.res.y)
        self.rept_recxx = round(self.cfg['reporttitle']['rect']['x1'] * self.res.x)
        self.rept_recyy = round(self.cfg['reporttitle']['rect']['y1'] * self.res.y)
        self.rept_spacing_x = round(self.cfg['reporttitle']['rect']['spacing_x'] * self.res.x)
        self.rept_spacing_y = round(self.cfg['reporttitle']['rect']['spacing_y'] * self.res.y)
        self.rept_fill = self.cfg['reporttitle']['rect']['fill']
        self.rept_tfill = self.cfg['reporttitle']['text']['fill']
        # name
        self.name_fnt = ImageFont.truetype(self.cfg['name']['font']['path'], self.cfg['name']['font']['size'])
        self.name_recx = round(self.cfg['name']['rect']['x0'] * self.res.x)
        self.name_recy = round(self.cfg['name']['rect']['y0'] * self.res.y)
        self.name_recxx = round(self.cfg['name']['rect']['x1'] * self.res.x)
        self.name_recyy = round(self.cfg['name']['rect']['y1'] * self.res.y)
        self.name_spacing_x = round(self.cfg['name']['rect']['spacing_x'] * self.res.x)
        self.name_spacing_y = round(self.cfg['name']['rect']['spacing_y'] * self.res.y)
        self.name_fill = self.cfg['name']['rect']['fill']
        self.name_tfill = self.cfg['name']['text']['fill']
        # job
        self.job_fnt = ImageFont.truetype(self.cfg['job']['font']['path'], self.cfg['job']['font']['size'])
        self.job_tfill = self.cfg['job']['fill']
        # crawl
        self.crw_fnt = ImageFont.truetype(self.cfg['crawl']['font']['path'], self.cfg['crawl']['font']['size'])
        self.crw_fnt_sz = self.cfg['crawl']['font']['size']
        self.crw_recx = round(self.cfg['crawl']['rect']['x0'] * self.res.x)
        self.crw_recy = round(self.cfg['crawl']['rect']['y0'] * self.res.y)
        self.crw_recxx = round(self.cfg['crawl']['rect']['x1'] * self.res.x)
        self.crw_recyy = round(self.cfg['crawl']['rect']['y1'] * self.res.y)
        self.crw_spacing_x = round(self.cfg['crawl']['rect']['spacing_x'] * self.res.x)
        self.crw_spacing_y = round(self.cfg['crawl']['rect']['spacing_y'] * self.res.y)
        self.crw_fill = self.cfg['crawl']['rect']['fill']
        self.crw_tfill = self.cfg['crawl']['text']['fill']
        # time
        self.time_fnt = ImageFont.truetype(self.cfg['time']['font']['path'], self.cfg['time']['font']['size'])
        self.time_recx = round(self.cfg['time']['rect']['x0'] * self.res.x)
        self.time_recy = round(self.cfg['time']['rect']['y0'] * self.res.y)
        self.time_recxx = round(self.cfg['time']['rect']['x1'] * self.res.x)
        self.time_recyy = round(self.cfg['time']['rect']['y1'] * self.res.y)
        self.time_spacing_x = round(self.cfg['time']['rect']['spacing_x'] * self.res.x)
        self.time_spacing_y = round(self.cfg['time']['rect']['spacing_y'] * self.res.y)
        self.time_fill = self.cfg['time']['rect']['fill']
        self.time_tfill = self.cfg['time']['text']['fill']
        self.time_tx = int(self.time_recx + self.time_spacing_x * 1.5)

    def load_cfg(self):
        with open(self.cfg_file, 'r') as f:
            self.cfg = yaml.load(f, Loader=yaml.FullLoader)

    def new_sample(self, img_path, img_name):
        self.s = Sample(img_path, img_name)
        self.img_name = img_name
        methodchoose = random.randint(0, 5)
        if methodchoose == 0:
            self.live()
        if methodchoose == 1:
            self.subtitles()
        if methodchoose == 2:
            self.source()
        if methodchoose == 3:
            self.reporttitle()
        if methodchoose == 4:
            self.namejob()
            self.timegenerator()
            if random.randint(0, 10) > 3:
                self.crawltext()
            else:
                self.resizedct()
        if methodchoose == 5:
            self.wildtext()
        self.s.image.save(self.cfg['annotation']['path'] + self.img_name + '.png')
        self.s.annotationsave(self.cfg['annotation']['path'])

    def getone(self, path):
        with open(path, "r") as file:
            file = list(file)
            file = [x.replace('\n', '') for x in file]
            return random.choice(file)

    def gettext(self, x, path):
        wordlist = self.loadfile(path)
        i = random.randint(0, len(wordlist) - 10)
        sentence = wordlist[i]
        sentencelength = len(sentence)
        senlen = random.randint(2, x)
        # print("len sentence", len(sentence))
        while len(sentence) < senlen and i < len(wordlist):
            i += 1
            if i >= len(wordlist) - 1: i = 0
            sentence = sentence + " " + wordlist[i]
        return sentence

    def loadfile(self, filename):
        with open(filename, "r") as file:
            file = list(file)
            words = []
            for sentence in file:
                word = sentence.split()
                for i in word:
                    words.append(i)
            wordlist = []
            for word in words:
                wordlist.append(word)
            return wordlist

    def getwildtext(self):
        rand = random.randint(0, 100)
        if rand < 10: return str(random.randint(0, 500000)) + self.getone(self.cfg['currency']['path'])
        if rand < 20: return self.getdate()
        if rand < 30: return str(random.randint(-40, 45)) + '°C'
        if rand < 40: return self.gettext(random.randint(10, 45), self.cfg['crawl']['path'])
        if rand < 50: return str("{:0>2d}".format(random.randint(0, 23))) + ':' + str(
            "{:0>2d}".format(random.randint(0, 59)))
        if rand < 60: return self.getpolitic(True)
        return self.gettext(random.randint(10, 70), self.cfg['reporttitle']['path'])

    def getdate(self):
        if random.randint(0, 1) == 0:
            return str(random.randint(1, 31)) + '.' + str(random.randint(1, 12)) + '.' + str(random.randint(1900, 2050))
        else:
            return str(random.randint(1, 31)) + '/' + str(random.randint(1, 12)) + '/' + str(random.randint(1900, 2050))

    def getpolitic(self, sure=False):
        with open(self.cfg['politic']['path'], "r") as file:
            file = list(file)
            file = [x.replace('\n', '') for x in file]
            if sure == False:
                if random.randint(0, 100) < self.cfg['politic']['chance']:
                    return (random.choice(file))
                else:
                    return 'null'
            else:
                return random.choice(file)

    def getplace(self):
        with open(self.cfg['place']['state']['path']) as file1, open(self.cfg['place']['town']['path']) as file2, open(
                self.cfg['place']['street']['path']) as file3:
            file1 = list(file1)
            file2 = list(file2)
            file3 = list(file3)
            file1 = [x.replace('\n', '') for x in file1]
            file2 = [x.replace('\n', '') for x in file2]
            file3 = [x.replace('\n', '') for x in file3]
            place = ''
            if random.randint(0, 1) == 1:
                place += random.choice(file1)
            if random.randint(0, 1) == 1:
                place += random.choice(file2) if place == '' else ', ' + random.choice(file2)
            if len(place) > 2:
                if random.randint(0, 1) == 1:
                    place += random.choice(ffile3) if place == '' else ', ' + random.choice(file3)
            else:
                place += random.choice(file3)
            return place

    def live(self):
        text = self.getplace()

        rect = Image.new('RGBA', self.s.image.size, (255, 255, 255, 0))
        d = ImageDraw.Draw(rect)

        recxx = self.live_recx + d.textsize(self.live_live, self.live_fnt)[
            0] + 2 * self.live_recspace_x  # self.cfg['live']['rect']['x1']*self.res.x
        recyy = self.live_recy + d.textsize(self.live_live, self.live_fnt)[
            1] + 2 * self.live_recspace_y  # self.cfg['live']['rect']['y1']*self.res.y
        ttx = recxx + 1 + self.live_recspace_x  # self.cfg['live']['text2']['x']*self.res.x
        tty = self.live_recy + self.live_recspace_y  # self.cfg['live']['text2']['y']*self.res.y

        d.rectangle([self.live_recx, self.live_recy, recxx, recyy], fill=self.live_recfill)
        d.rectangle(
            [recxx + 1, self.live_recy, recxx + d.textsize(text, self.live_fnt)[0] + 2 * self.live_recspace_x, recyy],
            fill=self.live_reccfill)

        self.s.image = Image.alpha_composite(self.s.image, rect)
        d = ImageDraw.Draw(self.s.image)

        d.text((self.live_tx, self.live_ty), self.live_live, font=self.live_fnt, fill=self.live_tfill)
        d.text((ttx, tty), text, font=self.live_fnt, fill=self.live_ttfill)

        self.s.annotation(self.live_tx, self.live_ty, self.live_live, self.live_fnt)
        self.s.annotation(ttx, tty, text, self.live_fnt)

    def subtitles(self):

        # make a blank image for the text, initialized to transparent text color
        rect = Image.new('RGBA', self.s.image.size, (255, 255, 255, 0))

        # get a drawing context
        d = ImageDraw.Draw(rect)

        text = self.gettext(self.sub_lines * ((self.sub_recxx - self.sub_recx) // (self.sub_fnt_sz // 2)),
                            self.cfg['reporttitle']['path'])
        lines = ((d.textsize(text, self.sub_fnt)[0]) // (self.sub_recxx - self.sub_recx - 2 * self.sub_spacing_x)) + 1
        if lines > self.sub_lines:
            lines = self.sub_lines
        recy = self.sub_recyy - 2 * self.sub_spacing_y - (lines - 1) * self.sub_spacing_bl - lines * \
               d.textsize(text, self.sub_fnt)[1]

        d.rectangle([self.sub_recx, recy, self.sub_recxx, self.sub_recyy], fill=self.sub_fill)

        self.s.image = Image.alpha_composite(self.s.image, rect)

        d = ImageDraw.Draw(self.s.image)
        j = 0
        textl = [''] * lines
        for i in range(lines):
            while d.textsize(textl[i], self.sub_fnt)[0] < self.sub_recxx - self.sub_recx - 2 * self.sub_spacing_x:
                if j > len(text): break
                textl[i] = text[0:j]
                j = j + 1
            text = text[j - 1:]
            j = 0

        for i in range(lines):
            tx = round(
                ((self.sub_recxx - self.sub_recx) / 2 + self.sub_recx) - d.textsize(textl[i], self.sub_fnt)[0] / 2)
            ty = recy + self.sub_spacing_y + i * self.sub_spacing_bl + i * d.textsize(textl[i], self.sub_fnt)[1]
            d.text((tx, ty), textl[i], font=self.sub_fnt, fill=self.sub_tfill)
            self.s.annotation(tx, ty, textl[i], font=self.sub_fnt)

    def source(self):
        # make a blank image for the text, initialized to transparent text color
        text = self.getone(self.cfg['source']['path'])
        rect = Image.new('RGBA', self.s.image.size, (255, 255, 255, 0))
        source = self.cfg['source']['source'] + ": " + text
        # get a font
        # get a drawing context
        d = ImageDraw.Draw(rect)
        textsize = d.textsize(source, self.sou_fnt)
        # draw text, half opacity
        d.rectangle([self.sou_recxx - 2 * self.sou_spacing_x - textsize[0],
                     self.sou_recyy - textsize[1] - 3 * self.sou_spacing_y, self.sou_recxx, self.sou_recyy],
                    fill=self.sou_fill)
        self.s.image = Image.alpha_composite(self.s.image, rect)
        d = ImageDraw.Draw(self.s.image)
        d.text((self.sou_recxx - self.sou_spacing_x - textsize[0], self.sou_recyy - self.sou_spacing_y - textsize[1]),
               source, font=self.sou_fnt, fill=self.sou_tfill)

        self.s.annotation(self.sou_recxx - self.sou_spacing_x - textsize[0],
                          self.sou_recyy - self.sou_spacing_y - textsize[1], source, self.sou_fnt)

    def reporttitle(self):
        # make a blank image for the text, initialized to transparent text color
        rect = Image.new('RGBA', self.s.image.size, (255, 255, 255, 0))
        # get a drawing context
        d = ImageDraw.Draw(rect)
        text = self.gettext((self.rept_recxx - self.rept_recx) // (self.rept_fnt_sz * 0.5),
                            self.cfg['reporttitle']['path'])
        textsize = d.textsize(text, self.rept_fnt)
        # draw text, half opacity
        while textsize[0] > self.rept_recxx - self.rept_recx - 2 * self.rept_spacing_x:
            text = self.gettext((self.rept_recxx - self.rept_recx) // (self.rept_fnt_sz * 0.5),
                                self.cfg['reporttitle']['path'])
        d.rectangle([self.rept_recx, self.rept_recy, self.rept_recxx, self.rept_recyy], fill=self.rept_fill)

        self.s.image = Image.alpha_composite(self.s.image, rect)

        d = ImageDraw.Draw(self.s.image)

        d.text((self.rept_recx + self.rept_spacing_x, self.rept_recy + self.rept_spacing_y), text, font=self.rept_fnt,
               fill=self.rept_tfill)

        self.s.annotation(self.rept_recx + self.rept_spacing_x, self.rept_recy + self.rept_spacing_y, text,
                          self.rept_fnt)

    def namejob(self):
        # make a blank image for the text, initialized to transparent text color
        first = self.getone(self.cfg['name']['first']['path'])
        last = self.getone(self.cfg['name']['last']['path'])
        politic = self.getone(self.cfg['politic']['path'])
        job = self.getone(self.cfg['job']['path'])
        rect = Image.new('RGBA', self.s.image.size, (255, 255, 255, 0))
        # get a drawing context
        d = ImageDraw.Draw(rect)
        # draw text, half opacity
        d.rectangle([self.name_recx, self.name_recy, self.name_recxx, self.name_recyy], fill=self.name_fill)
        self.s.image = Image.alpha_composite(self.s.image, rect)
        d = ImageDraw.Draw(self.s.image)

        if politic is 'null':
            text = first + " " + last + "      "
        else:
            text = first + " " + last + "  /" + politic + "/     "

        d.text((self.name_recx + self.name_spacing_x, self.name_recy + self.name_spacing_y), text, font=self.name_fnt,
               fill=self.name_tfill)
        self.s.annotation(self.name_recx + self.name_spacing_x, self.name_recy + self.name_spacing_y, text,
                          self.name_fnt)

        textsize = d.textsize(text, self.name_fnt)
        d.text((self.name_recx + self.name_spacing_x + textsize[0], self.name_recy + self.name_spacing_y), job,
               font=self.job_fnt, fill=self.job_tfill)

        self.s.annotation(self.name_recx + self.name_spacing_x + textsize[0], self.name_recy + self.name_spacing_y, job,
                          self.job_fnt)

    def crawltext(self):
        # make a blank image for the text, initialized to transparent text color
        rect = Image.new('RGBA', self.s.image.size, (255, 255, 255, 0))

        # get a font
        fnt = self.crw_fnt
        # get a drawing context
        d = ImageDraw.Draw(rect)
        text = self.gettext((self.crw_recxx - self.crw_recx) // (self.crw_fnt_sz // 2), self.cfg['crawl']['path'])
        # draw text, half opacity
        d.rectangle([self.crw_recx, self.crw_recy, self.crw_recxx, self.crw_recyy], fill=self.crw_fill)

        self.s.image = Image.alpha_composite(self.s.image, rect)

        d = ImageDraw.Draw(self.s.image)
        while d.textsize(text.upper(), fnt)[
            0] > self.crw_recxx - self.crw_recx - 2 * self.crw_spacing_x: text = self.gettext(
            (self.crw_recxx - self.crw_recx) // (self.crw_fnt_sz // 2), self.cfg['crawl']['path'])
        d.text((self.crw_recx + self.crw_spacing_x, self.crw_recy + self.crw_spacing_y), text.upper(), font=fnt,
               fill=self.crw_tfill)

        self.s.annotation(self.crw_recx + self.crw_spacing_x, self.crw_recy + self.crw_spacing_y, text.upper(), fnt)

    def resizedct(self):
        enlarcoef = random.randrange(10, 10 * self.cfg['resizedct']['enlarcoef']) / 10  # enlarge coeficient
        # make a blank image for the text, initialized to transparent text color
        self.s.image = self.s.image.resize((round(self.s.image.size[0] * enlarcoef), self.s.image.size[1]))

        rect = Image.new('RGBA', self.s.image.size, (255, 255, 255, 0))
        print(enlarcoef)
        # get a font
        fnt = self.crw_fnt
        # get a drawing context
        d = ImageDraw.Draw(rect)

        # draw text, half opacity
        d.rectangle(
            [round(self.crw_recx * enlarcoef), self.crw_recy, round(self.crw_recxx * enlarcoef), self.crw_recyy],
            fill=self.crw_fill)

        self.s.image = Image.alpha_composite(self.s.image, rect)
        text = self.gettext(enlarcoef * (self.crw_recxx - self.crw_recx) // (self.crw_fnt_sz // 2),
                            self.cfg['crawl']['path'])
        d = ImageDraw.Draw(self.s.image)
        while d.textsize(text.upper(), fnt)[0] > enlarcoef * (
                self.crw_recxx - self.crw_recx - 2 * self.crw_spacing_x): text = self.gettext(
            enlarcoef * (self.crw_recxx - self.crw_recx) // (self.crw_fnt_sz // 2), self.cfg['crawl']['path'])
        d.text((round(enlarcoef * (self.crw_recx + self.crw_spacing_x)), self.crw_recy + self.crw_spacing_y),
               text.upper(), font=fnt, fill=self.crw_tfill)

        self.s.image = self.s.image.resize((self.res.x, self.res.y))

        self.s.annotation(int(enlarcoef * (self.crw_recx + self.crw_spacing_x)), self.crw_recy + self.crw_spacing_y,
                          text.upper(), fnt, enlarcoef)

    def timegenerator(self):
        text = "{:02d}".format(randrange(24)) + ":" + "{:02d}".format(randrange(60))
        # text = "22" + ":" + "{:02d}".format(randrange(60))
        text = list(text)
        # make a blank image for the text, initialized to transparent text color
        rect = Image.new('RGBA', self.s.image.size, (255, 255, 255, 0))

        # get a font
        fnt = self.time_fnt
        # get a drawing context
        d = ImageDraw.Draw(rect)

        # draw text, half opacity
        d.rectangle([self.time_recx, self.time_recy, self.time_recxx, self.time_recyy], fill=self.time_fill)

        self.s.image = Image.alpha_composite(self.s.image, rect)

        d = ImageDraw.Draw(self.s.image)
        # img = Image.new('RGB', (100, 30), color = (73, 109, 137))

        d.text((self.time_tx, self.time_recy + self.time_spacing_y), text[0], font=fnt, fill=self.time_tfill)
        d.text((self.time_tx + self.time_spacing_x, self.time_recy + self.time_spacing_y), text[1], font=fnt,
               fill=self.time_tfill)
        d.text((self.time_tx + self.time_spacing_x * 2, self.time_recy + self.time_spacing_y), text[2], font=fnt,
               fill=self.time_tfill)
        d.text((self.time_tx + int(self.time_spacing_x * 2.6), self.time_recy + self.time_spacing_y), text[3], font=fnt,
               fill=self.time_tfill)
        d.text((self.time_tx + round(self.time_spacing_x * 3.6), self.time_recy + self.time_spacing_y), text[4],
               font=fnt, fill=self.time_tfill)

        self.s.annotation(self.time_tx, self.time_recy + self.time_spacing_y, text[0], fnt)
        self.s.annotation(self.time_tx + self.time_spacing_x, self.time_recy + self.time_spacing_y, text[1], fnt)
        self.s.annotation(self.time_tx + self.time_spacing_x * 2, self.time_recy + self.time_spacing_y, text[2], fnt)
        self.s.annotation(self.time_tx + round(self.time_spacing_x * 2.6), self.time_recy + self.time_spacing_y,
                          text[3], fnt)
        self.s.annotation(self.time_tx + round(self.time_spacing_x * 3.6), self.time_recy + self.time_spacing_y,
                          text[4], fnt)

    def syntwild(self):
        # make a blank image for the text, initialized to transparent text color
        rect = Image.new('RGBA', self.s.image.size, (255, 255, 255, 0))

        x = random.randint(int(self.res.x * 0.05), int(self.res.x * 0.7))
        y = random.randint(int(self.res.y * 0.05), int(self.res.y * 0.7))
        x2 = random.randint(int(self.res.x * 0.95) - (int(self.res.x * 0.90) - x), int(self.res.x * 0.95))
        y2 = random.randint(int(self.res.y * 0.95) - (int(self.res.y * 0.90) - y), int(self.res.y * 0.95))
        bcolor = self.getbackcolor()

        d = ImageDraw.Draw(rect)
        d.rectangle([x, y, x2, y2], fill=bcolor)
        # get a font
        font_size = random.randint(10, y2 - y if y2 - y < 40 else 40)
        # print(font_size)
        fontname = str(self.getone(self.cfg['syntwild']['fontlist']))
        fnt = ImageFont.truetype(fontname, font_size)
        # draw text, half opacity
        self.s.image = Image.alpha_composite(self.s.image, rect)
        d = ImageDraw.Draw(self.s.image)
        coordinates = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        wildtexts = [''] * 7
        errors = 0
        texterrors = 0
        ae = False
        for i in range(7):
            ae = False
            # print("nová interace i")
            wildtexts[i] = self.getwildtext()
            font_size = random.randint(10, y2 - y if y2 - y < 40 else 40)
            fontname = str(self.getone(self.cfg['syntwild']['fontlist']))
            fnt = ImageFont.truetype(fontname, font_size)
            while (x2 - x - d.textsize(wildtexts[i], fnt)[0]) < 1:
                texterrors += 1
                if errors > 100:
                    return False
                wildtexts[i] = self.getwildtext()
            coordinates[i][0] = x + random.randint(0, x2 - x - d.textsize(wildtexts[i], fnt)[0])
            coordinates[i][1] = y + random.randint(0, y2 - y - d.textsize(wildtexts[i], fnt)[1])
            coordinates[i][2] = coordinates[i][0] + d.textsize(wildtexts[i], fnt)[0]
            coordinates[i][3] = coordinates[i][1] + d.textsize(wildtexts[i], fnt)[1]
            if errors > 10: break
            for j in range(7):

                if i == j or i < j: break
                if errors > 10: break

                if d.textsize(wildtexts[i], fnt)[0] > x2 - x:
                    # print("chyba",font_size)
                    ae = True
                    break
                if (coordinates[i][0] < coordinates[j][2] and
                        coordinates[i][2] > coordinates[j][0] and
                        coordinates[i][1] < coordinates[j][3] and
                        coordinates[i][3] > coordinates[j][1]):
                    errors += 1
                    # ae is actual error
                    ae = True
                    break
            if ae == False:
                tcolor = self.gettextcolor()
                while self.checkcolors(bcolor, tcolor) == False:
                    tcolor = self.gettextcolor()
                # print("i=" + str(i)+"j="+str(j))
                d.text([coordinates[i][0], coordinates[i][1]], wildtexts[i], font=fnt, fill=tcolor)
                self.s.annotation(coordinates[i][0], coordinates[i][1], wildtexts[i], fnt)
        return True

    def wildtext(self):
        while self.syntwild() == False:
            self.syntwild()
        else:
            pass

    def gettextcolor(self):
        with open(self.cfg['textcolors']['path']) as f:
            barvytextu = [tuple(map(int, i.split(','))) for i in f]
        return random.choice(barvytextu)

    def getbackcolor(self):
        with open(self.cfg['backcolors']['path']) as f:
            barvypozadi = [tuple(map(int, i.split(','))) for i in f]
        return random.choice(barvypozadi)

    def checkcolors(self, bcolor, tcolor):
        diff = 0
        for i in range(2):
            diff += abs(bcolor[i] - tcolor[i])
        if diff < 150:
            return False
        else:
            return True


# In[68]:


a = AITGM('ct.yml')
a.new_sample('images/img1.jpg', 'test')
