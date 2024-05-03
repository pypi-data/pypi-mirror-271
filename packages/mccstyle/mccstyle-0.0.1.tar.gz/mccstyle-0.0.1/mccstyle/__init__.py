import ROOT

#
# Common values
textsize=0.045

# Apply ROOT style

# Canvas
ROOT.gStyle.SetHistTopMargin(0)
ROOT.gStyle.SetPadTickX(1)
ROOT.gStyle.SetPadTickY(1)

# Main title
ROOT.gStyle.SetTitleAlign(13)
ROOT.gStyle.SetTitleX(0.08)
ROOT.gStyle.SetTitleY(0.96)
ROOT.gStyle.SetTitleFontSize(textsize)

# Axis labels
ROOT.gStyle.SetLabelSize(textsize,"xyz")
ROOT.gStyle.SetTitleSize(textsize,"xyz")
ROOT.gStyle.SetTitleOffset(1.1,"y")

# Legend
ROOT.gStyle.SetLegendBorderSize(0)
ROOT.gStyle.SetLegendTextSize(textsize)

def logo(title=[],xpos=0.2,ypos=0.2,fontsize=0.05,sim=True,suffix=''):
    text=[]
    if suffix is None:
        text.append('#bf{Muon Collider}')
    else:
        text.append('#bf{Muon Collider} #it{%s}'%suffix)

    if sim:
        text.append("#it{Simulation}")

    if type(title)==list: text+=title
    elif title!=None: text.append(title)

    latext=None
    for i in range(len(text)):
        if latext is None: latext=text[i]
        else: latext='#splitline{%s}{%s}'%(latext,text[i])

    Tl=ROOT.TLatex()
    Tl.SetNDC()
    Tl.SetTextFont(42)
    Tl.DrawLatex(xpos, ypos, latext);

    return Tl
