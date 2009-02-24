/*
 * HDTV - A ROOT-based spectrum analysis software
 *  Copyright (C) 2006-2008  Norbert Braun <n.braun@ikp.uni-koeln.de>
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
 
#include "Util.h"

#include <sstream>

namespace HDTV {

static int num=0;

std::string GetFuncUniqueName(const char *prefix, void *ptr)
{
  // Constructs a unique name for a function by concatenation of an instance-unique prefix,
  // a textual representation of this, and an increasing number.
  // FIXME: not thread safe. The whole requirement of unique names is extremely ugly anyway.
  
  std::ostringstream name;
  name << prefix << "_" << ptr << "_" << ++num;
  
  return name.str();
}

} // end namespace HDTV
