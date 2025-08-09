/**
 * Academic Research UI Controller - Main Application Controller
 * 
 * This module serves as the main controller that composes and coordinates
 * all specialized UI modules for the academic research interface.
 * 
 * Educational Notes:
 * - Composition Pattern: Composes specialized modules into cohesive application
 * - Facade Pattern: Provides simple interface to complex subsystem interactions
 * - Coordinator Pattern: Manages communication between different UI modules
 * - Dependency Injection: Modules can be injected for testing and flexibility
 * - Event-Driven Architecture: Loosely coupled modules communicate via events
 * 
 * Design Patterns Applied:
 * - Facade Pattern: Simplifies interaction with multiple subsystems
 * - Mediator Pattern: Coordinates interactions between UI modules
 * - Observer Pattern: Responds to module state changes
 * - Strategy Pattern: Different UI strategies for different research contexts
 * - Factory Pattern: Creates appropriate UI components based on context
 * 
 * Academic Research Context:
 * - Research Workflow Integration: Seamless integration of all research tools
 * - Data Source Coordination: Manages multiple data sources and APIs
 * - User Journey Management: Guides users through complex research workflows
 * - State Synchronization: Keeps all UI components in sync
 * - Performance Optimization: Coordinates module loading and resource usage
 * 
 * Module Dependencies:
 * - AccessibilityManager: WCAG 2.1 compliance and inclusive design
 * - FilterManager: Advanced filtering and search capabilities
 * - VisualizationManager: D3.js visualizations and data displays
 * - DashboardManager: Research analytics and metrics
 * - ExportManager: Data export and citation management
 */

class AcademicResearchUI {
    constructor(options = {}) {
        // Application state
        this.state = {
            currentDomain: null,
            currentVisualizationType: 'sunburst',
            isLoading: false,
            userPreferences: {},
            activeModules: new Set(),
            initialized: false
        };
        
        // Module instances
        this.modules = {
            accessibility: null,
            filters: null,
            visualization: null,
            dashboard: null,
            evidence: null,
            export: null
        };
        
        // Configuration
        this.config = {
            autoInitialize: options.autoInitialize ?? true,
            enableAccessibility: options.enableAccessibility ?? true,
            enableAdvancedFilters: options.enableAdvancedFilters ?? true,
            enableVisualization: options.enableVisualization ?? true,
            enableDashboard: options.enableDashboard ?? true,
            enableEvidenceExplorer: options.enableEvidenceExplorer ?? true,
            enableExport: options.enableExport ?? true,
            debugMode: options.debugMode ?? false,
            ...options
        };
        
        // Event system for module communication
        this.eventBus = new EventTarget();
        
        // Initialize if configured to do so (moved outside constructor)
        if (this.config.autoInitialize) {
            // Use setTimeout to move async operation outside constructor
            setTimeout(() => this.initialize(), 0);
        }
    }

    /**
     * Initialize the complete academic research UI system
     * 
     * Educational Notes:
     * - Initialization Order: Critical modules (accessibility) load first
     * - Error Isolation: Module initialization failures don't break entire system
     * - Progressive Loading: Modules can be loaded progressively based on user needs
     * - State Management: Centralized initialization state tracking
     */
    async initialize() {
        if (this.state.initialized) {
            console.warn('Academic Research UI already initialized');
            return;
        }
        
        console.log('🎓 Initializing Academic Research UI System...');
        this.state.isLoading = true;
        
        try {
            // Phase 1: Initialize core accessibility features first
            await this.initializeAccessibility();
            
            // Phase 2: Initialize UI foundation modules
            await this.initializeCore();
            
            // Phase 3: Initialize specialized modules
            await this.initializeSpecializedModules();
            
            // Phase 4: Setup module communication and coordination
            this.setupModuleCommunication();
            
            // Phase 5: Load user preferences and restore state
            await this.loadUserPreferences();
            
            // Phase 6: Final setup and validation
            this.finalizeInitialization();
            
            this.state.initialized = true;
            this.state.isLoading = false;
            
            console.log('✅ Academic Research UI System ready');
            this.announceSystemReady();
            
        } catch (error) {
            console.error('❌ Academic Research UI initialization failed:', error);
            this.handleInitializationError(error);
        }
    }

    /**
     * Initialize accessibility features (Phase 1 - Critical)
     * 
     * Educational Notes:
     * - Accessibility First: Accessibility is not optional, it's foundational
     * - Early Initialization: Must be available before other UI interactions
     * - Error Handling: Accessibility failures are logged but don't break system
     */
    async initializeAccessibility() {
        if (!this.config.enableAccessibility) {
            console.log('Accessibility features disabled by configuration');
            return;
        }
        
        try {
            console.log('♿ Initializing accessibility features...');
            
            // Initialize accessibility manager
            if (typeof AccessibilityManager !== 'undefined') {
                this.modules.accessibility = new AccessibilityManager();
                this.state.activeModules.add('accessibility');
                console.log('✅ Accessibility Manager initialized');
            } else {
                console.warn('AccessibilityManager not available');
            }
            
        } catch (error) {
            console.error('❌ Accessibility initialization failed:', error);
            // Don't throw - accessibility failure shouldn't break entire system
        }
    }

    /**
     * Initialize core UI foundation modules (Phase 2)
     * 
     * Educational Notes:
     * - Foundation First: Core UI elements before specialized features
     * - Dependency Management: Ensures dependencies are available
     * - Graceful Degradation: System works even if some modules fail
     */
    async initializeCore() {
        console.log('🏗️ Initializing core UI modules...');
        
        // Initialize filter management
        await this.initializeFilterSystem();
        
        // Setup basic UI interactions
        this.setupBasicInteractions();
        
        // Initialize progress tracking
        this.initializeProgressTracking();
        
        console.log('✅ Core UI modules initialized');
    }

    /**
     * Initialize filter management system
     * 
     * Educational Notes:
     * - Filter Coordination: Central coordination of all filtering operations
     * - Real-Time Updates: Immediate UI updates as filters change
     * - State Persistence: Filter state maintained across sessions
     */
    async initializeFilterSystem() {
        if (!this.config.enableAdvancedFilters) {
            console.log('Advanced filters disabled by configuration');
            return;
        }
        
        try {
            if (typeof FilterManager !== 'undefined') {
                this.modules.filters = new FilterManager({
                    enableAdvancedFilters: this.config.enableAdvancedFilters,
                    debugMode: this.config.debugMode
                });
                
                // Subscribe to filter changes
                this.modules.filters.addObserver((changeEvent) => {
                    this.handleFilterChange(changeEvent);
                });
                
                this.state.activeModules.add('filters');
                console.log('✅ Filter Manager initialized');
            } else {
                console.warn('FilterManager not available');
            }
        } catch (error) {
            console.error('❌ Filter system initialization failed:', error);
        }
    }

    /**
     * Setup basic UI interactions
     * 
     * Educational Notes:
     * - Progressive Enhancement: Basic interactions work without advanced modules
     * - Event Delegation: Efficient event handling for dynamic content
     * - Keyboard Support: All interactions accessible via keyboard
     */
    setupBasicInteractions() {
        // Domain selector interactions
        this.setupDomainSelector();
        
        // Visualization type selection
        this.setupVisualizationControls();
        
        // User guidance and help systems
        this.setupUserGuidance();
        
        // Keyboard shortcuts
        this.setupKeyboardShortcuts();
    }

    /**
     * Setup domain selector with enhanced UX
     * 
     * Educational Notes:
     * - Progressive Disclosure: Advanced options revealed as needed
     * - Visual Feedback: Clear indication of selected domain
     * - Accessibility: Screen reader announcements for domain changes
     */
    setupDomainSelector() {
        const domainCards = document.querySelectorAll('.domain-card');
        
        domainCards.forEach(card => {
            card.addEventListener('click', (event) => {
                const domain = card.dataset.domain;
                this.selectDomain(domain);
            });
            
            // Keyboard support
            card.addEventListener('keydown', (event) => {
                if (event.key === 'Enter' || event.key === ' ') {
                    event.preventDefault();
                    const domain = card.dataset.domain;
                    this.selectDomain(domain);
                }
            });
            
            // Enhanced focus management
            card.setAttribute('tabindex', '0');
            card.setAttribute('role', 'button');
        });
    }

    /**
     * Select a research domain
     * 
     * @param {string} domain - Domain to select
     * 
     * Educational Notes:
     * - State Management: Centralized domain state management
     * - Event Broadcasting: Notifies other modules of domain change
     * - Visual Feedback: Updates UI to reflect selection
     */
    selectDomain(domain) {
        if (this.state.currentDomain === domain) return;
        
        console.log(`🎯 Selecting domain: ${domain}`);
        
        // Update state
        const previousDomain = this.state.currentDomain;
        this.state.currentDomain = domain;
        
        // Update UI
        this.updateDomainUI(domain, previousDomain);
        
        // Broadcast domain change to modules
        this.broadcastEvent('domain-changed', {
            domain,
            previousDomain,
            timestamp: Date.now()
        });
        
        // Announce to accessibility system
        this.announceChange(`Research domain changed to ${domain}`);
        
        // Load domain-specific data
        this.loadDomainData(domain);
    }

    /**
     * Update domain selection UI
     * 
     * @param {string} selectedDomain - Currently selected domain
     * @param {string} previousDomain - Previously selected domain
     * 
     * Educational Notes:
     * - Visual State Management: Clear visual indication of selection state
     * - Accessibility Updates: ARIA attributes updated for screen readers
     * - Animation Coordination: Smooth transitions between states
     */
    updateDomainUI(selectedDomain, previousDomain) {
        const cards = document.querySelectorAll('.domain-card');
        
        cards.forEach(card => {
            const domain = card.dataset.domain;
            const isSelected = domain === selectedDomain;
            
            // Update selection state
            card.classList.toggle('selected', isSelected);
            card.setAttribute('aria-selected', isSelected.toString());
            
            // Update visual indicators
            const checkIcon = card.querySelector('.check-icon');
            if (checkIcon) {
                checkIcon.style.display = isSelected ? 'block' : 'none';
            }
        });
        
        // Show visualization area
        const vizArea = document.getElementById('visualizationArea');
        if (vizArea) {
            vizArea.style.display = 'block';
            vizArea.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
        
        // Update progress tracker
        this.updateProgress(2);
    }

    /**
     * Setup visualization control interactions
     * 
     * Educational Notes:
     * - Visualization Strategy: Different visualization strategies for different data types
     * - Real-Time Updates: Immediate visualization updates as user changes options
     * - Accessibility: Full keyboard and screen reader support for visualization controls
     */
    setupVisualizationControls() {
        const vizOptions = document.querySelectorAll('.viz-option');
        
        vizOptions.forEach(option => {
            option.addEventListener('click', (event) => {
                const vizType = option.dataset.viz;
                this.selectVisualizationType(vizType);
            });
            
            // Keyboard support
            option.addEventListener('keydown', (event) => {
                if (event.key === 'Enter' || event.key === ' ') {
                    event.preventDefault();
                    const vizType = option.dataset.viz;
                    this.selectVisualizationType(vizType);
                }
            });
        });
    }

    /**
     * Select visualization type
     * 
     * @param {string} vizType - Type of visualization to display
     * 
     * Educational Notes:
     * - Visualization Strategy Pattern: Different rendering strategies for different viz types
     * - Performance Optimization: Lazy loading of visualization libraries
     * - State Synchronization: Keeps visualization state in sync with application state
     */
    selectVisualizationType(vizType) {
        if (this.state.currentVisualizationType === vizType) return;
        
        console.log(`📊 Selecting visualization type: ${vizType}`);
        
        // Update state
        const previousType = this.state.currentVisualizationType;
        this.state.currentVisualizationType = vizType;
        
        // Update UI
        this.updateVisualizationUI(vizType, previousType);
        
        // Broadcast change to modules
        this.broadcastEvent('visualization-type-changed', {
            vizType,
            previousType,
            domain: this.state.currentDomain,
            timestamp: Date.now()
        });
        
        // Announce change
        this.announceChange(`Visualization changed to ${vizType}`);
        
        // Load appropriate visualization
        this.loadVisualization(vizType);
    }

    /**
     * Initialize specialized modules (Phase 3)
     * 
     * Educational Notes:
     * - Modular Loading: Specialized modules loaded only when needed
     * - Dependency Injection: Modules can be injected for testing
     * - Error Isolation: Failures in specialized modules don't break core functionality
     */
    async initializeSpecializedModules() {
        console.log('🔧 Initializing specialized modules...');
        
        // Initialize modules in parallel for better performance
        const modulePromises = [];
        
        if (this.config.enableVisualization) {
            modulePromises.push(this.initializeVisualizationModule());
        }
        
        if (this.config.enableDashboard) {
            modulePromises.push(this.initializeDashboardModule());
        }
        
        if (this.config.enableEvidenceExplorer) {
            modulePromises.push(this.initializeEvidenceModule());
        }
        
        if (this.config.enableExport) {
            modulePromises.push(this.initializeExportModule());
        }
        
        // Wait for all modules to initialize
        await Promise.allSettled(modulePromises);
        
        console.log('✅ Specialized modules initialized');
    }

    /**
     * Initialize visualization module
     * 
     * Educational Notes:
     * - Lazy Loading: Visualization libraries loaded only when needed
     * - Memory Management: Proper cleanup of visualization resources
     * - Performance Optimization: Efficient rendering for large datasets
     */
    async initializeVisualizationModule() {
        try {
            if (typeof ConceptVisualization !== 'undefined') {
                this.modules.visualization = new ConceptVisualization();
                this.state.activeModules.add('visualization');
                console.log('✅ Visualization module initialized');
            } else {
                console.warn('ConceptVisualization not available');
            }
        } catch (error) {
            console.error('❌ Visualization module initialization failed:', error);
        }
    }

    /**
     * Initialize dashboard module
     * 
     * Educational Notes:
     * - Analytics Integration: Real-time research analytics and metrics
     * - Data Aggregation: Combines data from multiple sources
     * - Performance Monitoring: Tracks system performance metrics
     */
    async initializeDashboardModule() {
        try {
            if (typeof ResearchDashboard !== 'undefined') {
                this.modules.dashboard = new ResearchDashboard();
                this.state.activeModules.add('dashboard');
                console.log('✅ Dashboard module initialized');
            } else {
                console.warn('ResearchDashboard not available');
            }
        } catch (error) {
            console.error('❌ Dashboard module initialization failed:', error);
        }
    }

    /**
     * Initialize evidence explorer module
     * 
     * Educational Notes:
     * - Evidence Analysis: Deep dive into research evidence and citations
     * - Interactive Exploration: User-driven evidence discovery
     * - Academic Workflows: Specialized tools for academic research
     */
    async initializeEvidenceModule() {
        try {
            if (typeof EvidenceExplorer !== 'undefined') {
                this.modules.evidence = new EvidenceExplorer();
                this.state.activeModules.add('evidence');
                console.log('✅ Evidence explorer module initialized');
            } else {
                console.warn('EvidenceExplorer not available');
            }
        } catch (error) {
            console.error('❌ Evidence explorer module initialization failed:', error);
        }
    }

    /**
     * Initialize export module
     * 
     * Educational Notes:
     * - Data Export: Research-grade data export in multiple formats
     * - Citation Management: Proper academic citation formatting
     * - Format Support: Multiple export formats for different use cases
     */
    async initializeExportModule() {
        try {
            if (typeof ExportManager !== 'undefined') {
                this.modules.export = new ExportManager();
                this.state.activeModules.add('export');
                console.log('✅ Export module initialized');
            } else {
                console.warn('ExportManager not available');
            }
        } catch (error) {
            console.error('❌ Export module initialization failed:', error);
        }
    }

    /**
     * Setup communication between modules (Phase 4)
     * 
     * Educational Notes:
     * - Event-Driven Architecture: Loose coupling between modules
     * - Message Passing: Structured communication via events
     * - Error Isolation: Communication failures don't break modules
     */
    setupModuleCommunication() {
        console.log('📡 Setting up module communication...');
        
        // Setup filter change propagation
        this.eventBus.addEventListener('filter-changed', (event) => {
            this.propagateFilterChange(event.detail);
        });
        
        // Setup domain change propagation
        this.eventBus.addEventListener('domain-changed', (event) => {
            this.propagateDomainChange(event.detail);
        });
        
        // Setup visualization change propagation
        this.eventBus.addEventListener('visualization-type-changed', (event) => {
            this.propagateVisualizationChange(event.detail);
        });
        
        // Setup error handling
        this.eventBus.addEventListener('module-error', (event) => {
            this.handleModuleError(event.detail);
        });
        
        console.log('✅ Module communication established');
    }

    /**
     * Propagate filter changes to all relevant modules
     * 
     * @param {object} changeDetail - Filter change details
     * 
     * Educational Notes:
     * - Change Propagation: Ensures all modules stay in sync
     * - Performance Optimization: Only notifies modules that need updates
     * - Error Handling: Individual module failures don't break propagation
     */
    propagateFilterChange(changeDetail) {
        const { filters } = changeDetail;
        
        // Update visualization
        if (this.modules.visualization?.applyFilters) {
            try {
                this.modules.visualization.applyFilters(filters);
            } catch (error) {
                console.error('Error applying filters to visualization:', error);
            }
        }
        
        // Update dashboard
        if (this.modules.dashboard?.updateFilters) {
            try {
                this.modules.dashboard.updateFilters(filters);
            } catch (error) {
                console.error('Error applying filters to dashboard:', error);
            }
        }
        
        // Update evidence explorer
        if (this.modules.evidence?.applyFilters) {
            try {
                this.modules.evidence.applyFilters(filters);
            } catch (error) {
                console.error('Error applying filters to evidence explorer:', error);
            }
        }
    }

    /**
     * Handle filter changes from filter manager
     * 
     * @param {object} changeEvent - Filter change event
     * 
     * Educational Notes:
     * - Observer Pattern: Responds to filter manager changes
     * - Event Coordination: Coordinates filter changes across UI
     * - State Synchronization: Keeps application state in sync
     */
    handleFilterChange(changeEvent) {
        console.log('🔍 Handling filter change:', changeEvent);
        
        // Broadcast to other modules via event bus
        this.broadcastEvent('filter-changed', {
            filters: changeEvent.allFilters,
            changedFilter: changeEvent.key,
            newValue: changeEvent.newValue,
            previousValue: changeEvent.previousValue,
            timestamp: changeEvent.timestamp
        });
        
        // Update progress if this is first filter applied
        if (Object.keys(changeEvent.allFilters).some(key => 
            changeEvent.allFilters[key] !== this.modules.filters.defaultFilters[key])) {
            this.updateProgress(3);
        }
    }

    /**
     * Load user preferences and restore state (Phase 5)
     * 
     * Educational Notes:
     * - Personalization: Remembers user preferences across sessions
     * - State Restoration: Restores complex application state
     * - Privacy: Only saves preferences, not personal research data
     */
    async loadUserPreferences() {
        try {
            const preferences = this.loadPreferences();
            this.state.userPreferences = preferences;
            
            // Apply preferences to modules
            await this.applyUserPreferences(preferences);
            
            console.log('✅ User preferences loaded');
        } catch (error) {
            console.error('❌ Failed to load user preferences:', error);
        }
    }

    /**
     * Load preferences from storage
     * 
     * @returns {object} User preferences
     * 
     * Educational Notes:
     * - Data Persistence: Uses localStorage for preference storage
     * - Error Handling: Graceful fallback to defaults
     * - Privacy: No personal data stored, only interface preferences
     */
    loadPreferences() {
        try {
            const stored = localStorage.getItem('academic-ui-preferences');
            return stored ? JSON.parse(stored) : {};
        } catch (error) {
            console.warn('Could not load user preferences:', error);
            return {};
        }
    }

    /**
     * Apply user preferences to modules
     * 
     * @param {object} preferences - User preferences to apply
     * 
     * Educational Notes:
     * - Preference Application: Applies preferences to appropriate modules
     * - Module Coordination: Ensures all modules respect user preferences
     * - Fallback Handling: Graceful handling of invalid preferences
     */
    async applyUserPreferences(preferences) {
        // Apply to accessibility module
        if (this.modules.accessibility && preferences.accessibility) {
            this.modules.accessibility.preferences = {
                ...this.modules.accessibility.preferences,
                ...preferences.accessibility
            };
            this.modules.accessibility.applyAccessibilityPreferences();
        }
        
        // Apply to filter module
        if (this.modules.filters && preferences.filters) {
            Object.keys(preferences.filters).forEach(key => {
                if (this.modules.filters.filters.hasOwnProperty(key)) {
                    this.modules.filters.filters[key] = preferences.filters[key];
                }
            });
            this.modules.filters.updateFilterUI();
        }
        
        // Apply general UI preferences
        if (preferences.ui) {
            this.applyUIPreferences(preferences.ui);
        }
    }

    /**
     * Apply general UI preferences
     * 
     * @param {object} uiPreferences - UI preferences to apply
     * 
     * Educational Notes:
     * - UI Customization: Allows users to customize interface
     * - State Consistency: Ensures UI state matches preferences
     * - Progressive Enhancement: Preferences enhance default experience
     */
    applyUIPreferences(uiPreferences) {
        // Apply domain preference
        if (uiPreferences.lastDomain) {
            this.selectDomain(uiPreferences.lastDomain);
        }
        
        // Apply visualization preference
        if (uiPreferences.lastVisualizationType) {
            this.selectVisualizationType(uiPreferences.lastVisualizationType);
        }
        
        // Apply layout preferences
        if (uiPreferences.layout) {
            this.applyLayoutPreferences(uiPreferences.layout);
        }
    }

    /**
     * Finalize initialization (Phase 6)
     * 
     * Educational Notes:
     * - System Validation: Ensures all critical systems are working
     * - Performance Metrics: Tracks initialization performance
     * - User Feedback: Provides feedback on system readiness
     */
    finalizeInitialization() {
        // Validate critical modules
        this.validateCriticalModules();
        
        // Setup performance monitoring
        this.setupPerformanceMonitoring();
        
        // Show initial state
        this.showInitialState();
        
        // Setup periodic health checks
        this.setupHealthChecks();
    }

    /**
     * Validate that critical modules are working
     * 
     * Educational Notes:
     * - System Validation: Ensures system integrity
     * - Error Detection: Early detection of configuration issues
     * - Fallback Planning: Prepares fallback strategies for failed modules
     */
    validateCriticalModules() {
        const criticalModules = ['accessibility', 'filters'];
        const failedModules = [];
        
        criticalModules.forEach(moduleName => {
            if (!this.state.activeModules.has(moduleName)) {
                failedModules.push(moduleName);
            }
        });
        
        if (failedModules.length > 0) {
            console.warn('Critical modules failed to initialize:', failedModules);
            this.handleCriticalModuleFailures(failedModules);
        }
    }

    /**
     * Setup performance monitoring
     * 
     * Educational Notes:
     * - Performance Tracking: Monitors system performance metrics
     * - User Experience: Identifies performance bottlenecks
     * - Continuous Improvement: Data for system optimization
     */
    setupPerformanceMonitoring() {
        if (this.config.debugMode) {
            this.performanceMonitor = {
                startTime: performance.now(),
                moduleLoadTimes: new Map(),
                userInteractions: []
            };
            
            // Track module performance
            this.state.activeModules.forEach(moduleName => {
                const module = this.modules[moduleName];
                if (module?.getPerformanceMetrics) {
                    this.performanceMonitor.moduleLoadTimes.set(moduleName, 
                        module.getPerformanceMetrics());
                }
            });
        }
    }

    /**
     * Show initial application state
     * 
     * Educational Notes:
     * - User Onboarding: Guides new users through system capabilities
     * - State Visualization: Shows current system state clearly
     * - Progressive Disclosure: Reveals functionality as users need it
     */
    showInitialState() {
        // Show empty state if no domain selected
        if (!this.state.currentDomain) {
            this.showEmptyState();
        }
        
        // Initialize progress tracking
        this.initializeProgressTracking();
        
        // Setup user guidance
        this.setupUserGuidance();
    }

    /**
     * Show empty state with guidance
     * 
     * Educational Notes:
     * - Empty State Design: Guides users when no data is available
     * - Call to Action: Clear next steps for users
     * - Accessibility: Screen reader friendly empty state
     */
    showEmptyState() {
        const emptyState = document.getElementById('emptyState');
        if (emptyState) {
            emptyState.style.display = 'block';
        }
        
        const vizArea = document.getElementById('visualizationArea');
        if (vizArea) {
            vizArea.style.display = 'none';
        }
        
        // Announce empty state to screen readers
        this.announceChange('Welcome to the Academic Research Interface. Select a research domain to begin.');
    }

    /**
     * Initialize progress tracking system
     * 
     * Educational Notes:
     * - User Journey: Tracks user progress through research workflow
     * - Visual Feedback: Progress indicators help users understand next steps
     * - Accessibility: Progress announced to screen readers
     */
    initializeProgressTracking() {
        this.progressSteps = document.querySelectorAll('.step');
        this.currentStep = 1;
        
        // Set initial state
        this.updateProgress(1);
    }

    /**
     * Update user journey progress
     * 
     * @param {number} step - Current step number
     * 
     * Educational Notes:
     * - Progress Visualization: Clear indication of user progress
     * - State Management: Tracks progress state across interactions
     * - Accessibility: Progress changes announced to users
     */
    updateProgress(step) {
        if (step === this.currentStep) return;
        
        this.progressSteps.forEach((stepEl, index) => {
            const stepNumber = index + 1;
            
            if (stepNumber < step) {
                stepEl.classList.add('completed');
                stepEl.classList.remove('active');
            } else if (stepNumber === step) {
                stepEl.classList.add('active');
                stepEl.classList.remove('completed');
            } else {
                stepEl.classList.remove('active', 'completed');
            }
        });
        
        this.currentStep = step;
        
        // Announce progress change
        this.announceChange(`Progress updated: step ${step}`);
    }

    /**
     * Setup user guidance system
     * 
     * Educational Notes:
     * - User Experience: Contextual help and guidance
     * - Progressive Disclosure: Help appears when needed
     * - Accessibility: Help content fully accessible
     */
    setupUserGuidance() {
        // Setup quick actions
        this.setupQuickActions();
        
        // Setup help system
        this.setupHelpSystem();
        
        // Setup tooltips and hints
        this.setupTooltips();
    }

    /**
     * Setup quick action buttons
     * 
     * Educational Notes:
     * - Quick Actions: Common tasks easily accessible
     * - User Efficiency: Reduces clicks for common operations
     * - Keyboard Support: All actions keyboard accessible
     */
    setupQuickActions() {
        const quickActions = document.querySelectorAll('.quick-action');
        
        quickActions.forEach(action => {
            action.addEventListener('click', (event) => {
                const actionType = action.dataset.action;
                this.handleQuickAction(actionType);
            });
            
            // Keyboard support
            action.addEventListener('keydown', (event) => {
                if (event.key === 'Enter' || event.key === ' ') {
                    event.preventDefault();
                    const actionType = action.dataset.action;
                    this.handleQuickAction(actionType);
                }
            });
        });
    }

    /**
     * Handle quick action execution
     * 
     * @param {string} actionType - Type of quick action to execute
     * 
     * Educational Notes:
     * - Action Handling: Centralized handling of user actions
     * - State Management: Actions update application state appropriately
     * - Feedback: Users receive immediate feedback on actions
     */
    handleQuickAction(actionType) {
        console.log(`⚡ Executing quick action: ${actionType}`);
        
        switch (actionType) {
            case 'load-sample':
                this.loadSampleData();
                break;
            case 'reset-filters':
                if (this.modules.filters) {
                    this.modules.filters.resetFilters();
                }
                break;
            case 'export-results':
                this.exportResults();
                break;
            case 'show-help':
                this.showHelp();
                break;
            default:
                console.warn(`Unknown quick action: ${actionType}`);
        }
        
        // Announce action completion
        this.announceChange(`${actionType} action completed`);
    }

    /**
     * Setup keyboard shortcuts
     * 
     * Educational Notes:
     * - Power User Support: Efficient keyboard navigation
     * - Accessibility: Alternative to mouse-based interactions
     * - Standard Conventions: Follows common keyboard shortcut patterns
     */
    setupKeyboardShortcuts() {
        document.addEventListener('keydown', (event) => {
            // Skip if user is in an input field
            if (event.target.tagName === 'INPUT' || event.target.tagName === 'TEXTAREA') {
                return;
            }
            
            // Ctrl/Cmd + H: Show help
            if ((event.ctrlKey || event.metaKey) && event.key === 'h') {
                event.preventDefault();
                this.showHelp();
            }
            
            // Ctrl/Cmd + R: Reset view
            if ((event.ctrlKey || event.metaKey) && event.key === 'r') {
                event.preventDefault();
                this.resetView();
            }
            
            // Ctrl/Cmd + E: Export results
            if ((event.ctrlKey || event.metaKey) && event.key === 'e') {
                event.preventDefault();
                this.exportResults();
            }
            
            // Escape: Close modals/overlays
            if (event.key === 'Escape') {
                this.handleEscape();
            }
        });
    }

    /**
     * Load sample data for demonstration
     * 
     * Educational Notes:
     * - User Onboarding: Helps users understand system capabilities
     * - Demo Data: Realistic sample data for exploration
     * - Progressive Loading: Data loaded progressively for better UX
     */
    async loadSampleData() {
        console.log('📊 Loading sample data...');
        
        try {
            this.state.isLoading = true;
            this.showLoadingState(true);
            
            // Simulate API call delay
            await new Promise(resolve => setTimeout(resolve, 1000));
            
            // Load sample data into appropriate modules
            if (this.modules.visualization) {
                await this.modules.visualization.loadSampleData();
            }
            
            if (this.modules.dashboard) {
                await this.modules.dashboard.loadSampleData();
            }
            
            this.state.isLoading = false;
            this.showLoadingState(false);
            
            // Update progress
            this.updateProgress(4);
            
            console.log('✅ Sample data loaded');
            this.announceChange('Sample data loaded successfully');
            
        } catch (error) {
            console.error('❌ Failed to load sample data:', error);
            this.handleError('Failed to load sample data');
        }
    }

    /**
     * Reset view to initial state
     * 
     * Educational Notes:
     * - State Reset: Returns to known good state
     * - User Recovery: Helps users recover from complex states
     * - Module Coordination: Resets all modules consistently
     */
    resetView() {
        console.log('🔄 Resetting view...');
        
        // Reset domain selection
        this.state.currentDomain = null;
        this.state.currentVisualizationType = 'sunburst';
        
        // Reset all modules
        Object.values(this.modules).forEach(module => {
            if (module?.reset) {
                try {
                    module.reset();
                } catch (error) {
                    console.error('Error resetting module:', error);
                }
            }
        });
        
        // Reset UI
        this.resetUI();
        
        // Reset progress
        this.updateProgress(1);
        
        this.announceChange('View reset to initial state');
    }

    /**
     * Reset UI elements to initial state
     * 
     * Educational Notes:
     * - UI State Management: Consistent UI reset across components
     * - Visual Feedback: Clear indication of reset state
     * - Accessibility: Reset announced to screen readers
     */
    resetUI() {
        // Reset domain cards
        document.querySelectorAll('.domain-card').forEach(card => {
            card.classList.remove('selected');
            card.setAttribute('aria-selected', 'false');
        });
        
        // Reset visualization options
        document.querySelectorAll('.viz-option').forEach(option => {
            option.classList.remove('active');
            option.setAttribute('aria-selected', 'false');
        });
        
        // Show empty state
        this.showEmptyState();
    }

    /**
     * Export research results
     * 
     * Educational Notes:
     * - Data Export: Research-grade data export capabilities
     * - Format Support: Multiple export formats for different needs
     * - Academic Standards: Proper citation and metadata inclusion
     */
    exportResults() {
        console.log('📤 Exporting results...');
        
        if (this.modules.export) {
            this.modules.export.showExportDialog();
        } else {
            // Fallback export functionality
            this.showBasicExportOptions();
        }
        
        this.announceChange('Export options opened');
    }

    /**
     * Show basic export options when export module unavailable
     * 
     * Educational Notes:
     * - Graceful Degradation: Basic functionality when advanced modules unavailable
     * - User Experience: Users can still export even with limited functionality
     * - Progressive Enhancement: Advanced features enhance basic functionality
     */
    showBasicExportOptions() {
        // Create simple export modal
        const modal = document.createElement('div');
        modal.className = 'modal fade';
        modal.innerHTML = `
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">Export Results</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <p>Choose export format:</p>
                        <button class="btn btn-primary me-2" onclick="window.print()">Print</button>
                        <button class="btn btn-outline-primary" onclick="this.exportJSON()">JSON</button>
                    </div>
                </div>
            </div>
        `;
        
        document.body.appendChild(modal);
        
        // Show modal
        const bootstrapModal = new bootstrap.Modal(modal);
        bootstrapModal.show();
        
        // Cleanup on close
        modal.addEventListener('hidden.bs.modal', () => {
            document.body.removeChild(modal);
        });
    }

    /**
     * Show help information
     * 
     * Educational Notes:
     * - User Support: Contextual help for complex interfaces
     * - Progressive Disclosure: Help content organized by topic
     * - Accessibility: Help content fully accessible with proper headings
     */
    showHelp() {
        console.log('❓ Showing help...');
        
        // Implementation would show help modal or sidebar
        this.announceChange('Help information displayed');
    }

    /**
     * Handle escape key press
     * 
     * Educational Notes:
     * - Keyboard Interaction: Standard escape key behavior
     * - Modal Management: Proper modal and overlay dismissal
     * - User Experience: Quick way to close overlays
     */
    handleEscape() {
        // Close any open modals
        const openModals = document.querySelectorAll('.modal.show');
        openModals.forEach(modal => {
            const modalInstance = bootstrap.Modal.getInstance(modal);
            if (modalInstance) {
                modalInstance.hide();
            }
        });
        
        // Close any open dropdowns
        const openDropdowns = document.querySelectorAll('.dropdown-menu.show');
        openDropdowns.forEach(dropdown => {
            dropdown.classList.remove('show');
        });
    }

    /**
     * Show loading state
     * 
     * @param {boolean} isLoading - Whether to show loading state
     * 
     * Educational Notes:
     * - User Feedback: Clear indication of system processing
     * - Accessibility: Loading state announced to screen readers
     * - Performance: Visual feedback during slow operations
     */
    showLoadingState(isLoading) {
        const loadingIndicator = document.querySelector('.loading-indicator');
        if (loadingIndicator) {
            loadingIndicator.style.display = isLoading ? 'block' : 'none';
        }
        
        // Disable interactive elements during loading
        const interactiveElements = document.querySelectorAll('button, input, select');
        interactiveElements.forEach(el => {
            el.disabled = isLoading;
        });
        
        if (isLoading) {
            this.announceChange('Loading data...');
        }
    }

    /**
     * Broadcast event to module communication system
     * 
     * @param {string} eventType - Type of event to broadcast
     * @param {object} detail - Event detail data
     * 
     * Educational Notes:
     * - Event-Driven Architecture: Decoupled module communication
     * - Message Passing: Structured data passing between modules
     * - Error Isolation: Event failures don't break broadcasting
     */
    broadcastEvent(eventType, detail) {
        try {
            this.eventBus.dispatchEvent(new CustomEvent(eventType, { detail }));
        } catch (error) {
            console.error(`Failed to broadcast event ${eventType}:`, error);
        }
    }

    /**
     * Announce change to accessibility system
     * 
     * @param {string} message - Message to announce
     * @param {boolean} urgent - Whether this is an urgent announcement
     * 
     * Educational Notes:
     * - Accessibility Integration: Works with accessibility manager
     * - User Feedback: Keeps screen reader users informed
     * - Context Awareness: Different announcement strategies for different contexts
     */
    announceChange(message, urgent = false) {
        if (this.modules.accessibility?.announce) {
            this.modules.accessibility.announce(message, urgent);
        } else {
            // Fallback announcement
            console.log(`📢 ${urgent ? 'URGENT' : 'INFO'}: ${message}`);
        }
    }

    /**
     * Announce system ready state
     * 
     * Educational Notes:
     * - System Status: Informs users when system is ready
     * - Accessibility: Important for screen reader users
     * - User Confidence: Clear indication system is working
     */
    announceSystemReady() {
        this.announceChange('Academic Research Interface is ready. You can now select a research domain to begin.');
    }

    /**
     * Handle initialization errors
     * 
     * @param {Error} error - Initialization error
     * 
     * Educational Notes:
     * - Error Handling: Graceful handling of initialization failures
     * - User Communication: Clear error messages for users
     * - System Recovery: Attempts to provide fallback functionality
     */
    handleInitializationError(error) {
        console.error('System initialization failed:', error);
        
        this.state.isLoading = false;
        
        // Show error message to user
        this.showErrorMessage('System initialization failed. Some features may not be available.');
        
        // Attempt to provide basic functionality
        this.enableBasicFunctionality();
    }

    /**
     * Handle errors from individual modules
     * 
     * @param {object} errorDetail - Error details from module
     * 
     * Educational Notes:
     * - Error Isolation: Module errors don't break entire system
     * - Error Recovery: Attempts to recover from individual module failures
     * - User Communication: Informs users of any limitations
     */
    handleModuleError(errorDetail) {
        const { moduleName, error } = errorDetail;
        
        console.error(`Module error in ${moduleName}:`, error);
        
        // Disable failed module
        this.state.activeModules.delete(moduleName);
        this.modules[moduleName] = null;
        
        // Inform user if critical module failed
        const criticalModules = ['accessibility', 'filters'];
        if (criticalModules.includes(moduleName)) {
            this.showErrorMessage(`${moduleName} module failed. Some features may not work properly.`);
        }
    }

    /**
     * Show error message to user
     * 
     * @param {string} message - Error message to display
     * 
     * Educational Notes:
     * - User Communication: Clear, non-technical error messages
     * - Accessibility: Error messages announced to screen readers
     * - Recovery Guidance: Helps users understand next steps
     */
    showErrorMessage(message) {
        // Show in UI
        const errorContainer = document.querySelector('.error-container');
        if (errorContainer) {
            errorContainer.textContent = message;
            errorContainer.style.display = 'block';
        }
        
        // Announce to screen readers
        this.announceChange(message, true);
    }

    /**
     * Enable basic functionality when advanced modules fail
     * 
     * Educational Notes:
     * - Graceful Degradation: Basic functionality when advanced features fail
     * - User Experience: Users can still accomplish core tasks
     * - System Resilience: System remains usable despite failures
     */
    enableBasicFunctionality() {
        // Enable basic domain selection
        this.setupDomainSelector();
        
        // Enable basic visualization controls
        this.setupVisualizationControls();
        
        // Show degraded state notice
        this.showDegradedStateNotice();
    }

    /**
     * Show notice about degraded functionality
     * 
     * Educational Notes:
     * - Transparency: Users know about system limitations
     * - Expectation Management: Sets appropriate user expectations
     * - Recovery Options: Provides options for full functionality
     */
    showDegradedStateNotice() {
        const notice = document.createElement('div');
        notice.className = 'alert alert-warning';
        notice.innerHTML = `
            <strong>Limited Functionality:</strong> 
            Some advanced features are not available. 
            Try refreshing the page to restore full functionality.
        `;
        
        const container = document.querySelector('.main-content');
        if (container) {
            container.insertBefore(notice, container.firstChild);
        }
    }

    /**
     * Get current application state
     * 
     * @returns {object} Current application state
     * 
     * Educational Notes:
     * - State Access: Provides read-only access to application state
     * - Module Integration: Allows modules to access current state
     * - Debugging: Useful for debugging and monitoring
     */
    getState() {
        return {
            ...this.state,
            moduleStates: this.getModuleStates(),
            performance: this.getPerformanceMetrics()
        };
    }

    /**
     * Get state from all active modules
     * 
     * @returns {object} Combined module states
     * 
     * Educational Notes:
     * - State Aggregation: Combines state from all modules
     * - Module Introspection: Allows inspection of module states
     * - Debugging Support: Helpful for debugging complex interactions
     */
    getModuleStates() {
        const moduleStates = {};
        
        Object.keys(this.modules).forEach(moduleName => {
            const module = this.modules[moduleName];
            if (module && typeof module.getState === 'function') {
                try {
                    moduleStates[moduleName] = module.getState();
                } catch (error) {
                    console.error(`Failed to get state from ${moduleName}:`, error);
                    moduleStates[moduleName] = { error: error.message };
                }
            }
        });
        
        return moduleStates;
    }

    /**
     * Get performance metrics
     * 
     * @returns {object} Performance metrics
     * 
     * Educational Notes:
     * - Performance Monitoring: Tracks system performance
     * - Optimization: Data for system optimization
     * - User Experience: Identifies performance bottlenecks
     */
    getPerformanceMetrics() {
        if (!this.performanceMonitor) {
            return null;
        }
        
        return {
            totalInitTime: performance.now() - this.performanceMonitor.startTime,
            moduleLoadTimes: Object.fromEntries(this.performanceMonitor.moduleLoadTimes),
            activeModules: Array.from(this.state.activeModules),
            userInteractions: this.performanceMonitor.userInteractions.length
        };
    }

    /**
     * Save current state and preferences
     * 
     * Educational Notes:
     * - State Persistence: Saves user preferences and application state
     * - Privacy: Only saves preferences, not personal research data
     * - Recovery: Enables state restoration after page reload
     */
    saveState() {
        try {
            const preferences = {
                ui: {
                    lastDomain: this.state.currentDomain,
                    lastVisualizationType: this.state.currentVisualizationType
                }
            };
            
            // Add module preferences
            if (this.modules.accessibility) {
                preferences.accessibility = this.modules.accessibility.preferences;
            }
            
            if (this.modules.filters) {
                preferences.filters = this.modules.filters.getCurrentFilters();
            }
            
            localStorage.setItem('academic-ui-preferences', JSON.stringify(preferences));
            console.log('State saved successfully');
            
        } catch (error) {
            console.error('Failed to save state:', error);
        }
    }

    /**
     * Cleanup and destroy the UI system
     * 
     * Educational Notes:
     * - Resource Management: Proper cleanup of resources and event listeners
     * - Memory Management: Prevents memory leaks in single-page applications
     * - Module Cleanup: Ensures all modules clean up properly
     */
    destroy() {
        console.log('🧹 Cleaning up Academic Research UI...');
        
        // Save current state
        this.saveState();
        
        // Cleanup modules
        Object.values(this.modules).forEach(module => {
            if (module && typeof module.destroy === 'function') {
                try {
                    module.destroy();
                } catch (error) {
                    console.error('Error destroying module:', error);
                }
            }
        });
        
        // Clear event listeners
        this.eventBus.removeEventListener('filter-changed', this.propagateFilterChange);
        this.eventBus.removeEventListener('domain-changed', this.propagateDomainChange);
        this.eventBus.removeEventListener('visualization-type-changed', this.propagateVisualizationChange);
        this.eventBus.removeEventListener('module-error', this.handleModuleError);
        
        // Clear state
        this.state = null;
        this.modules = {};
        this.performanceMonitor = null;
        
        console.log('✅ Academic Research UI cleaned up');
    }
}

// Export for module systems
if (typeof module !== 'undefined' && module.exports) {
    module.exports = AcademicResearchUI;
}

// Global instantiation for direct script inclusion
if (typeof window !== 'undefined') {
    window.AcademicResearchUI = AcademicResearchUI;
    
    // Auto-initialize if DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => {
            window.academicUI = new AcademicResearchUI();
        });
    } else {
        window.academicUI = new AcademicResearchUI();
    }
}
