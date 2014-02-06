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

#ifndef APPLICATIONFACTORY_H
#define APPLICATIONFACTORY_H

#include <string>
#include <omniORB4/CORBA.h>

#include <ossie/CF/cf.h>
#include <ossie/CF/StandardEvent.h>
#include <ossie/SoftwareAssembly.h>
#include <ossie/debug.h>
#include <ossie/prop_utils.h>
#include <ossie/prop_helpers.h>

#include "PersistenceStore.h"
#include "applicationSupport.h"
#include "connectionSupport.h"

class DomainManager_impl;
class Application_impl;

class createHelper;

class ApplicationFactory_impl: public virtual POA_CF::ApplicationFactory
{
    ENABLE_LOGGING

private:
    ApplicationFactory_impl();  // Node default constructor
    ApplicationFactory_impl(ApplicationFactory_impl&);  // No copying

    std::string _name;
    std::string _identifier;
    std::string _softwareProfile;

    CosNaming::NamingContext_var _domainContext;

    ossie::SoftwareAssembly _sadParser;
    CF::FileManager_var     _fileMgr;
    CF::DomainManager_var   _dmnMgr;

    boost::mutex _pendingCreateLock;

    std::string         _domainName;
    std::string         _domainManagerName;
    DomainManager_impl* _domainManager;

    unsigned short _lastWaveformUniqueId;
    // Support for creating a new waveform naming context
    std::string getWaveformContextName(std::string name);
    std::string getBaseWaveformContext(std::string waveform_context);

public:
    ApplicationFactory_impl (
        const char*                             softwareProfile, 
        CF::DomainManager::ApplicationSequence* unused, 
        std::string                             domainName, 
        std::string                             domainManagerName, 
        DomainManager_impl*                     domainManager);
    ~ApplicationFactory_impl ();

    CF::Application_ptr create (const char* name,
                                const CF::Properties& initConfiguration,
                                const CF::DeviceAssignmentSequence& deviceAssignments)
    throw (CF::ApplicationFactory::InvalidInitConfiguration,
           CF::ApplicationFactory::CreateApplicationRequestError,
           CF::ApplicationFactory::CreateApplicationInsufficientCapacityError,
           CF::ApplicationFactory::CreateApplicationError,
           CORBA::SystemException);

    // getters for attributes
    char* name () throw (CORBA::SystemException) {
        return CORBA::string_dup(_name.c_str());
    }

    char* identifier () throw (CORBA::SystemException) {
        return CORBA::string_dup(_identifier.c_str());
    }

    char* softwareProfile () throw (CORBA::SystemException) {
        return CORBA::string_dup(_softwareProfile.c_str());
    }

    const ossie::SoftwareAssembly& getSadParser() const {
        return _sadParser;
    };


    // allow createHelper to have access to ApplicationFactory_impl
    friend class createHelper;

};
#endif

#ifndef CREATEHELPER_H
#define CREATEHELPER_H

class createHelper:
public ossie::ComponentLookup,
public ossie::DeviceLookup
{

public:
    createHelper (const ApplicationFactory_impl& appFact,
                  std::string waveformContextName,
                  std::string base_naming_context,
                  CosNaming::NamingContext_ptr WaveformContext);
    ~createHelper ();

    CF::Application_ptr create (const char* name,
                                const CF::Properties& initConfiguration,
                                const CF::DeviceAssignmentSequence& deviceAssignments)
    throw (CF::ApplicationFactory::InvalidInitConfiguration,
           CF::ApplicationFactory::CreateApplicationRequestError,
           CF::ApplicationFactory::CreateApplicationError,
           CORBA::SystemException);

private:

    // List of used devices assignments
    typedef std::vector< ossie::DeviceAssignmentInfo >                 DeviceAssignmentList;

    // Capacity allocation relation, device -> property set
    typedef ossie::AllocPropsInfo                                      CapacityAllocation;

    // List of capacity allocations
    typedef std::vector< CapacityAllocation >                          CapacityAllocationList;

    // mapping of capacity allocations derived from a compoenent
    typedef std::map< std::string, CapacityAllocationList >            CapacityAllocationTable;

    // list of components that are part of a collocation
    typedef std::vector <ossie::ComponentInfo* >                       PlacementList;

    // Used for storing the current state of the OE & create process
    const ApplicationFactory_impl& _appFact;
 
    //
    // List of allocated capacities (i.e. property settings) set against assigned devices
    //
    //CapacityAllocationTable _appCapacityTable;
    //CapacityAllocationList _usesDeviceCapacities;
    CF::AllocationManager::AllocationResponseSequence _allocationResponses;

    ossie::DeviceList _registeredDevices;
    PlacementList     _requiredComponents;
    ossie::DeviceList _remoteDevices;

    //
    // List of used devices allocated during application creation
    //
    DeviceAssignmentList          _appUsedDevs;
    std::vector<CF::Resource_ptr> _startSeq;
    std::vector<std::string>      _startOrderIds;
    
    CF::Application::ComponentProcessIdSequence _pidSeq;
    std::map<std::string, std::string>          _fileTable;

    // mapping of component id to filenames/device id tuple
    std::map<std::string, std::pair<std::string, std::string> > _loadedComponentTable; 
    
    // mapping of component id to filenames/device id tuple
    std::map<std::string, std::pair<std::string, unsigned long> > _runningComponentTable; 

    // waveform instance-specific naming context (unique to the instance of the waveform)
    std::string _waveformContextName; 

    // full (includes full context path) waveform instance-specific naming context
    std::string _baseNamingContext; 

    // CORBA naming context
    CosNaming::NamingContext_var _waveformContext; 

    CF::Application::ComponentElementSequence _namingCtxSeq;
    CF::Application::ComponentElementSequence _implSeq;

    ossie::ApplicationInfo _appInfo;

    // createHelper helper methods
    void overrideAssemblyControllerProperties(
        const CF::Properties& initConfiguration,
        ossie::ComponentInfo*& assemblyControllerComponent);
    void overrideExternalProperties(const CF::Properties& initConfiguration);
    void overrideProperties(
        const CF::Properties& initConfiguration,
        ossie::ComponentInfo*& component);
    void attemptDeviceAssignmentToComponent(
        const PlacementList&       placingComponents,
        const ossie::DeviceIDList& devList,
        const std::string&         collocationId,
        std::string&               c_id,
        CapacityAllocationTable&   collocCapacities,
        DeviceAssignmentList&      collocAssignedDevs);
    void assignRemainingComponentsToDevices(
        const CF::DeviceAssignmentSequence& deviceAssignments);
    void initialize(void);
    void checkRegisteredDevicesSize(const char* name);
    void _assignComponentsUsingDAS(
        const CF::DeviceAssignmentSequence& deviceAssignments);
    void _getComponentsToPlace(
        const std::vector<ossie::ComponentPlacement>& collocatedComponents,
        ossie::DeviceIDList&                          assignedDevices,
        PlacementList&                                placingComponents);
    void _loadAndExecuteComponents();
    void _initializeComponents(CF::Resource_var& assemblyController);
    void _connectComponents(
        std::vector<ossie::ConnectionNode>& connections);
    void _configureComponents();
    void _printComponentIDs(
        PlacementList& placingComponents, 
        ossie::SoftwareAssembly::HostCollocation& collocation) const;
    void _checkAssemblyController(
        CF::Resource_var&      assemblyController,
        ossie::ComponentInfo*& assemblyControllerComponent) const;
    void setUpExternalPorts(std::auto_ptr<Application_impl>& application);
    void setUpExternalProperties(
        std::auto_ptr<Application_impl>& application);
    void _handleHostCollocation();
    void _handleUsesDevices(const std::string& appName);
    void _resolveImplementations(PlacementList::iterator comp, PlacementList& compList, std::vector<ossie::ImplementationInfo::List> &res_vec);
    void _removeUnmatchedImplementations(std::vector<ossie::ImplementationInfo::List> &res_vec);
    void _consolidateAllocations(std::vector<ossie::ImplementationInfo::List> &res_vec, std::vector<CF::Properties>& allocs);
    void _evaluateMATHinRequest(CF::Properties &request, CF::Properties configureProperties);
    void _expandDevicePrf(CF::AllocationManager::AllocationResponseType response, ossie::Properties& devicePRF);
    void _assembleRequestProperties(CF::AllocationManager::AllocationRequestType &request, std::vector<ossie::SPD::PropertyRef> &prop_refs,
            ossie::ImplementationInfo* impl);
    void _castRequestProperties(CF::AllocationManager::AllocationRequestType &request, const std::vector<ossie::SPD::PropertyRef> &prop_refs,
            unsigned int offset=0);
    void _castRequestProperties(CF::AllocationManager::AllocationRequestType &request, const std::vector<ossie::SoftwareAssembly::PropertyRef> &prop_refs,
            unsigned int offset=0);
    CF::DataType castProperty(const ossie::ComponentProperty* property);

    // Populate _requiredComponents vector
    void getRequiredComponents() throw (CF::ApplicationFactory::CreateApplicationError); 

    void getDeviceImplementations(std::vector<ossie::SPD::Implementation>&, const CF::DeviceAssignmentSequence&);

    // Supports allocation
    CF::AllocationManager::AllocationResponseSequence* allocateUsesDeviceProperties(
        ossie::ImplementationInfo* component_impl,
        unsigned int usesDevIdx,
        CF::Properties &allocatedProps,
        const CF::Properties& configureProperties);
    CF::AllocationManager::AllocationResponseSequence* allocateUsesDeviceProperties(
        ossie::ComponentInfo* component,
        unsigned int usesDevIdx,
        CF::Properties &allocatedProps,
        const CF::Properties& configureProperties);
    void allocateComponent(ossie::ComponentInfo* component,
                           const CF::DeviceAssignmentSequence& deviceAssignments,
                           DeviceAssignmentList    &appAssignedDevices,
                           bool cleanup=true );

    CF::AllocationManager::AllocationResponseSequence* allocateComponentToDevice(ossie::ComponentInfo* component,
                                   ossie::ImplementationInfo* implementation,
                                   const CF::DeviceAssignmentSequence& deviceAssignments,
                                   ossie::Properties& devicePRF );

    bool resolveSoftpkgDependencies(
        ossie::ImplementationInfo* implementation, 
        CF::Device_ptr             device,
        ossie::Properties&         devicePRF)
            throw (CF::ApplicationFactory::CreateApplicationError);
    
    bool checkImplementationDependencyMatch(
        ossie::ImplementationInfo&       implementation_1, 
        const ossie::ImplementationInfo& implementation_2, 
        CF::Device_ptr device,
        ossie::Properties& devicePRF);
 
    // Supports loading, executing, initializing, configuring, & connecting
    void loadAndExecuteComponents(
        CF::Application::ComponentProcessIdSequence*                   pid, 
        std::map<std::string, std::string>*                            fileTable,
        CosNaming::NamingContext_ptr                                   WaveformContext,
        std::map<std::string, std::pair<std::string, std::string> >*   loadedComponentTable,
        std::map<std::string, std::pair<std::string, unsigned long> >* runningComponentTable);

    void attemptComponentExecution (
        const boost::filesystem::path&                                  executeName,
        const CF::ExecutableDevice_var&                                 execdev,
        ossie::ComponentInfo*&                                          component,
        const ossie::ImplementationInfo*&                               implementation,
        CF::Application::ComponentProcessIdSequence*&                   pid,
        std::map<std::string, std::pair<std::string, unsigned long> >*& runningComponentTable);

    void initializeComponents(
        CF::Resource_var&            assemblyController, 
        CosNaming::NamingContext_ptr WaveformContext);

    void addComponentsToApplication(Application_impl* application);
    void configureComponents();
    void connectComponents(
        std::vector<ossie::ConnectionNode>& connections, 
        std::string                         base_naming_context);

    // Functions for looking up particular components/devices
    CF::Device_ptr find_device_from_id(const char*);
    const ossie::DeviceNode& find_device_node_from_id(const char*) throw(std::exception);
    CF::DeviceManager_ptr find_devicemgr_for_device(CF::Device_ptr device);
    ossie::ComponentInfo* findComponentByInstantiationId(const std::string& identifier);

    // Cleanup - used when create fails/doesn't succeed for some reason
    bool _alreadyCleaned;
    void _cleanupLoadAndExecuteComponents();
    void _cleanupNewContext();
    void _cleanupCollocation( CapacityAllocationTable & collocCapacities, DeviceAssignmentList & collocAssignedDevs);
    void _cleanupAllocateDevices();
    void _cleanupRequiredComponents();
    void _cleanupResourceNotFound();
    void _cleanupAssemblyControllerInitializeFailed();
    void _cleanupAssemblyControllerConfigureFailed();
    void _cleanupResourceInitializeFailed();
    void _cleanupResourceConfigureFailed();
    void _cleanupApplicationCreateFailed();
    void _cleanupConnectionFailed();
    void _undoCapacityAllocations( CapacityAllocationList & alloc_set );
    
    // Shutdown - clean up memory
    void _deleteRequiredComponents();

    /** Implements the ConnectionManager functions
     *  - Makes this class compatible with the ConnectionManager
     */
    // ComponentLookup interface
    CF::Resource_ptr lookupComponentByInstantiationId(const std::string& identifier);
    CF::DeviceManager_ptr lookupDeviceManagerByInstantiationId(const std::string& identifier);
    CosEventChannelAdmin::EventChannel_ptr lookupEventChannel(const std::string &EventChannelName);
    unsigned int incrementEventChannelConnections(const std::string &EventChannelName);
    unsigned int decrementEventChannelConnections(const std::string &EventChannelName);

    // DeviceLookup interface
    CF::Device_ptr lookupDeviceThatLoadedComponentInstantiationId(const std::string& componentId);
    CF::Device_ptr lookupDeviceUsedByComponentInstantiationId(
        const std::string& componentId, 
        const std::string& usesId);
    CF::Device_ptr lookupDeviceUsedByApplication(const std::string& usesRefId);
};
#endif
