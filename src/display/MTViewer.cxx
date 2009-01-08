/*
 * HDTV - A ROOT-based spectrum analysis software
 *  Copyright (C) 2006-2009  Norbert Braun <n.braun@ikp.uni-koeln.de>
 *
 * This file is part of HDTV.
 *
 * HDTV is free software; you can redistribute it and/or modify it
 * under the terms of the GNU General Public License as published by the
 * Free Software Foundation; either version 2 of the License, or (at your
 * option) any later version.
 *
 * HDTV is distributed in the hope that it will be useful, but WITHOUT
 * ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
 * FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
 * for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with HDTV; if not, write to the Free Software Foundation,
 * Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA
 * 
 */

#include "MTViewer.h"

namespace HDTV {
namespace Display {

MTViewer::MTViewer(UInt_t w, UInt_t h, TH2 *mat, const char *title)
  : TGMainFrame(gClient->GetRoot(), w, h)
{
  fView = new HDTV::Display::View2D(this, w-4, h-4, mat);
  AddFrame(fView, new TGLayoutHints(kLHintsExpandX | kLHintsExpandY, 0,0,0,0));
  
  fStatusBar = new TGStatusBar(this, 10, 16);
  AddFrame(fStatusBar, new TGLayoutHints(kLHintsExpandX, 0,0,0,0));
  
  fView->SetStatusBar(fStatusBar);

  SetWindowName(title);
  MapSubwindows();
  Resize(GetDefaultSize());
  MapWindow();
}

MTViewer::~MTViewer()
{
  Cleanup();
}

} // end namespace Display
} // end namespace HDTV

int main()
{ return 0; }
