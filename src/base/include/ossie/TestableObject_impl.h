/*
 * This file is protected by Copyright. Please refer to the COPYRIGHT file 
 * distributed with this source distribution.
 * 
 * This file is part of REDHAWK core.
 * 
 * REDHAWK core is free software: you can redistribute it and/or modify it 
 * under the terms of the GNU Lesser General Public License as published by the 
 * Free Software Foundation, either version 3 of the License, or (at your 
 * option) any later version.
 * 
 * REDHAWK core is distributed in the hope that it will be useful, but WITHOUT 
 * ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or 
 * FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License 
 * for more details.
 * 
 * You should have received a copy of the GNU Lesser General Public License 
 * along with this program.  If not, see http://www.gnu.org/licenses/.
 */


#ifndef TESTABLEOBJECT_IMPL_H
#define TESTABLEOBJECT_IMPL_H

#include "ossiecf.h"

#include "CF/cf.h"

/**

The testable object interface provides a means to perform stand alone testing
of an SCA component. This function is useful for built in test (BIT)
operations.
*/

class OSSIECF_API TestableObject_impl: public virtual
    POA_CF::TestableObject
{
public:
    TestableObject_impl () { }

    /// Run the test specified by TestID with the values supplied in testValues.
    void runTest (CORBA::ULong TestID, CF::Properties& testValues)
    throw (CF::UnknownProperties, CF::TestableObject::UnknownTest,
           CORBA::SystemException);
};
#endif                                            /*  */
