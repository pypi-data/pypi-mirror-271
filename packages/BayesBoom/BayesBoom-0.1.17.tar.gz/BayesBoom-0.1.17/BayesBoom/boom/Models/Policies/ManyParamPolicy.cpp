// Copyright 2018 Google LLC. All Rights Reserved.
/*
  Copyright (C) 2005 Steven L. Scott

  This library is free software; you can redistribute it and/or
  modify it under the terms of the GNU Lesser General Public
  License as published by the Free Software Foundation; either
  version 2.1 of the License, or (at your option) any later version.

  This library is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
  Lesser General Public License for more details.

  You should have received a copy of the GNU Lesser General Public
  License along with this library; if not, write to the Free Software
  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA
*/
#include "Models/Policies/ManyParamPolicy.hpp"

namespace BOOM {
  namespace {
    typedef ManyParamPolicy MPP;
  }  // namespace

  MPP::ManyParamPolicy() {}

  MPP::ManyParamPolicy(const MPP &rhs) : Model(rhs) {}

  ManyParamPolicy &MPP::operator=(const ManyParamPolicy &rhs) {
    if (&rhs != this) {
      clear();
    }
    return *this;
  }

}  // namespace BOOM
