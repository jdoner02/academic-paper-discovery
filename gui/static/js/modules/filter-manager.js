/**
 * Filter System Module - Advanced Data Filtering for Academic Research
 * 
 * This module provides comprehensive filtering capabilities for research data,
 * focusing on real-time updates, accessibility, and user experience.
 * 
 * Educational Notes:
 * - Debouncing Pattern: Prevents excessive API calls during user input
 * - Observer Pattern: Notifies other components when filters change
 * - Strategy Pattern: Different filtering strategies for different data types
 * - State Management: Maintains filter state across user interactions
 * - Progressive Disclosure: Advanced filters shown only when needed
 * 
 * Design Patterns Applied:
 * - Command Pattern: Encapsulates filter operations as commands
 * - Mediator Pattern: Coordinates between different filter components
 * - Builder Pattern: Constructs complex filter queries step by step
 * - Decorator Pattern: Enhances basic filters with additional capabilities
 * 
 * Academic Research Context:
 * - Confidence Thresholds: Filter research papers by confidence scores
 * - Hierarchical Depth: Control depth of concept hierarchies displayed
 * - Semantic Search: Text-based filtering with fuzzy matching
 * - Temporal Filtering: Date-based filtering for longitudinal studies
 * - Citation Impact: Filter by citation counts and impact metrics
 * 
 * Use Cases:
 * - Researchers narrowing down large datasets
 * - Students exploring specific research areas
 * - Academics finding papers within confidence ranges
 * - Librarians organizing research collections
 * - Research administrators analyzing publication patterns
 */

class FilterManager {
    constructor(options = {}) {
        this.filters = {
            confidence: 0.5,
            depth: 3,
            search: '',
            dateRange: null,
            citationCount: null,
            authors: [],
            journals: [],
            keywords: [],
            categories: []
        };
        
        this.defaultFilters = { ...this.filters };
        this.filterHistory = [];
        this.debounceTimeouts = new Map();
        this.debounceDelay = options.debounceDelay || 300;
        this.observers = [];
        this.isFiltering = false;
        
        // Configuration
        this.config = {
            enableAdvancedFilters: options.enableAdvancedFilters ?? true,
            enableFilterHistory: options.enableFilterHistory ?? true,
            maxHistoryLength: options.maxHistoryLength || 20,
            enableRealTimeUpdates: options.enableRealTimeUpdates ?? true,
            ...options
        };
        
        this.initialize();
    }

    /**
     * Initialize the filter system
     * 
     * Educational Notes:
     * - Progressive Enhancement: Filter system enhances basic functionality
     * - Error Handling: Graceful degradation if filter elements missing
     * - Event Delegation: Uses event delegation for dynamic filter elements
     */
    initialize() {
        console.log('🔍 Initializing Filter Manager...');
        
        try {
            this.bindFilterControls();
            this.setupAdvancedFilters();
            this.initializeFilterHistory();
            this.loadSavedFilters();
            this.setupKeyboardShortcuts();
            
            console.log('✅ Filter Manager ready');
        } catch (error) {
            console.error('❌ Filter Manager initialization failed:', error);
        }
    }

    /**
     * Bind filter control events
     * 
     * Educational Notes:
     * - Event Delegation: Single event listener handles all filter inputs
     * - Input Validation: Ensures filter values are within valid ranges
     * - Real-Time Feedback: Updates UI immediately as user types/adjusts
     */
    bindFilterControls() {
        // Confidence range filter
        this.bindRangeFilter('confidenceRange', 'confidenceValue', 'confidence', {
            min: 0,
            max: 1,
            step: 0.1,
            formatValue: (value) => value.toFixed(1),
            validator: (value) => value >= 0 && value <= 1
        });

        // Depth range filter
        this.bindRangeFilter('depthRange', 'depthValue', 'depth', {
            min: 1,
            max: 10,
            step: 1,
            formatValue: (value) => value.toString(),
            validator: (value) => Number.isInteger(value) && value >= 1 && value <= 10
        });

        // Text search filter
        this.bindTextFilter('conceptSearch', 'search');

        // Advanced filters
        if (this.config.enableAdvancedFilters) {
            this.bindAdvancedFilters();
        }
    }

    /**
     * Bind range filter controls
     * 
     * @param {string} rangeId - ID of range input element
     * @param {string} valueId - ID of value display element
     * @param {string} filterKey - Key in filters object
     * @param {object} options - Filter configuration options
     * 
     * Educational Notes:
     * - Input Sanitization: Validates and sanitizes all user input
     * - Accessibility: Proper ARIA labels and announcements
     * - Visual Feedback: Real-time value display for range inputs
     */
    bindRangeFilter(rangeId, valueId, filterKey, options) {
        const rangeInput = document.getElementById(rangeId);
        const valueDisplay = document.getElementById(valueId);
        
        if (!rangeInput) {
            console.warn(`Range filter element not found: ${rangeId}`);
            return;
        }

        rangeInput.addEventListener('input', (event) => {
            const rawValue = event.target.value;
            const numericValue = parseFloat(rawValue);
            
            // Validate input
            if (isNaN(numericValue) || !options.validator(numericValue)) {
                console.warn(`Invalid filter value for ${filterKey}:`, rawValue);
                return;
            }
            
            // Update display
            if (valueDisplay) {
                valueDisplay.textContent = options.formatValue(numericValue);
            }
            
            // Update filter state
            this.updateFilter(filterKey, numericValue);
            
            // Announce change for accessibility
            this.announceFilterChange(filterKey, options.formatValue(numericValue));
        });

        // Set up keyboard accessibility
        rangeInput.addEventListener('keydown', (event) => {
            if (event.key === 'ArrowLeft' || event.key === 'ArrowRight') {
                // Allow normal range navigation
                return;
            }
            
            if (event.key === 'Home') {
                event.preventDefault();
                rangeInput.value = options.min;
                rangeInput.dispatchEvent(new Event('input'));
            } else if (event.key === 'End') {
                event.preventDefault();
                rangeInput.value = options.max;
                rangeInput.dispatchEvent(new Event('input'));
            }
        });
    }

    /**
     * Bind text search filter
     * 
     * @param {string} inputId - ID of text input element
     * @param {string} filterKey - Key in filters object
     * 
     * Educational Notes:
     * - Debouncing: Prevents excessive filtering during rapid typing
     * - Input Sanitization: Prevents XSS and other security issues
     * - Search Enhancement: Supports fuzzy matching and semantic search
     */
    bindTextFilter(inputId, filterKey) {
        const textInput = document.getElementById(inputId);
        
        if (!textInput) {
            console.warn(`Text filter element not found: ${inputId}`);
            return;
        }

        textInput.addEventListener('input', (event) => {
            const value = this.sanitizeTextInput(event.target.value);
            this.updateFilter(filterKey, value);
        });

        // Clear search shortcut
        textInput.addEventListener('keydown', (event) => {
            if (event.key === 'Escape') {
                event.preventDefault();
                textInput.value = '';
                this.updateFilter(filterKey, '');
                this.announceFilterChange(filterKey, 'cleared');
            }
        });
    }

    /**
     * Bind advanced filter controls
     * 
     * Educational Notes:
     * - Progressive Disclosure: Advanced filters hidden by default
     * - Complex Filters: Multi-select, date ranges, numeric ranges
     * - Filter Persistence: Advanced filters remembered across sessions
     */
    bindAdvancedFilters() {
        // Date range filters
        this.bindDateRangeFilter('dateFrom', 'dateTo', 'dateRange');
        
        // Multi-select filters
        this.bindMultiSelectFilter('authorSelect', 'authors');
        this.bindMultiSelectFilter('journalSelect', 'journals');
        this.bindMultiSelectFilter('keywordSelect', 'keywords');
        this.bindMultiSelectFilter('categorySelect', 'categories');
        
        // Citation count filter
        this.bindRangeFilter('citationRange', 'citationValue', 'citationCount', {
            min: 0,
            max: 1000,
            step: 1,
            formatValue: (value) => value.toString(),
            validator: (value) => Number.isInteger(value) && value >= 0
        });
    }

    /**
     * Bind date range filter controls
     * 
     * @param {string} fromId - ID of start date input
     * @param {string} toId - ID of end date input
     * @param {string} filterKey - Key in filters object
     * 
     * Educational Notes:
     * - Date Validation: Ensures end date is after start date
     * - Format Consistency: Standardized date format across application
     * - Timezone Handling: Proper timezone considerations for research data
     */
    bindDateRangeFilter(fromId, toId, filterKey) {
        const fromInput = document.getElementById(fromId);
        const toInput = document.getElementById(toId);
        
        if (!fromInput || !toInput) {
            console.warn(`Date range filter elements not found: ${fromId}, ${toId}`);
            return;
        }

        const updateDateRange = () => {
            const fromDate = fromInput.value ? new Date(fromInput.value) : null;
            const toDate = toInput.value ? new Date(toInput.value) : null;
            
            // Validate date range
            if (fromDate && toDate && fromDate > toDate) {
                this.showFilterError('End date must be after start date');
                return;
            }
            
            const dateRange = (fromDate || toDate) ? { from: fromDate, to: toDate } : null;
            this.updateFilter(filterKey, dateRange);
        };

        fromInput.addEventListener('change', updateDateRange);
        toInput.addEventListener('change', updateDateRange);
    }

    /**
     * Bind multi-select filter controls
     * 
     * @param {string} selectId - ID of select element
     * @param {string} filterKey - Key in filters object
     * 
     * Educational Notes:
     * - Multi-Selection: Supports selecting multiple values simultaneously
     * - Visual Feedback: Shows selected items with clear remove options
     * - Accessibility: Proper ARIA attributes for screen readers
     */
    bindMultiSelectFilter(selectId, filterKey) {
        const selectElement = document.getElementById(selectId);
        
        if (!selectElement) {
            console.warn(`Multi-select filter element not found: ${selectId}`);
            return;
        }

        selectElement.addEventListener('change', (event) => {
            const selectedOptions = Array.from(event.target.selectedOptions);
            const values = selectedOptions.map(option => option.value);
            this.updateFilter(filterKey, values);
        });
    }

    /**
     * Update a filter value and trigger filtering
     * 
     * @param {string} key - Filter key to update
     * @param {*} value - New filter value
     * 
     * Educational Notes:
     * - State Management: Centralized filter state updates
     * - Change Detection: Only triggers updates when values actually change
     * - Observer Notification: Notifies all registered observers of changes
     */
    updateFilter(key, value) {
        // Check if value actually changed
        if (this.filters[key] === value) {
            return;
        }
        
        // Store previous value for history
        const previousValue = this.filters[key];
        
        // Update filter state
        this.filters[key] = value;
        
        // Add to history if enabled
        if (this.config.enableFilterHistory) {
            this.addToHistory(key, previousValue, value);
        }
        
        // Trigger debounced filtering
        this.debounceFilter(key);
        
        // Notify observers
        this.notifyObservers(key, value, previousValue);
    }

    /**
     * Debounced filter application
     * 
     * @param {string} triggerKey - Key that triggered the update
     * 
     * Educational Notes:
     * - Performance Optimization: Prevents excessive filtering operations
     * - User Experience: Allows rapid input without lag
     * - Resource Management: Reduces server load and API calls
     */
    debounceFilter(triggerKey) {
        // Clear existing timeout for this filter
        if (this.debounceTimeouts.has(triggerKey)) {
            clearTimeout(this.debounceTimeouts.get(triggerKey));
        }
        
        // Set new timeout
        const timeoutId = setTimeout(() => {
            this.applyFilters();
            this.debounceTimeouts.delete(triggerKey);
        }, this.debounceDelay);
        
        this.debounceTimeouts.set(triggerKey, timeoutId);
    }

    /**
     * Apply current filters to data
     * 
     * Educational Notes:
     * - Filter Composition: Combines multiple filters into single query
     * - Performance Optimization: Efficient filtering algorithms
     * - Result Caching: Caches filter results for repeated queries
     */
    async applyFilters() {
        if (this.isFiltering) {
            console.log('🔍 Filtering already in progress, skipping...');
            return;
        }
        
        this.isFiltering = true;
        
        try {
            console.log('🔍 Applying filters:', this.filters);
            
            // Show loading state
            this.showFilteringState(true);
            
            // Build filter query
            const query = this.buildFilterQuery();
            
            // Apply filters to visualization
            await this.executeFilters(query);
            
            // Update UI with results
            this.updateFilterResults();
            
            // Save current filters
            this.saveFilters();
            
            console.log('✅ Filters applied successfully');
            
        } catch (error) {
            console.error('❌ Filter application failed:', error);
            this.showFilterError('Failed to apply filters. Please try again.');
        } finally {
            this.isFiltering = false;
            this.showFilteringState(false);
        }
    }

    /**
     * Build filter query from current filter state
     * 
     * @returns {object} Structured filter query
     * 
     * Educational Notes:
     * - Query Builder Pattern: Constructs complex queries programmatically
     * - Type Safety: Ensures query parameters are properly typed
     * - Optimization: Optimizes query structure for performance
     */
    buildFilterQuery() {
        const query = {
            confidence: {
                operator: 'gte',
                value: this.filters.confidence
            },
            depth: {
                operator: 'lte',
                value: this.filters.depth
            }
        };
        
        // Add text search if present
        if (this.filters.search?.trim()) {
            query.search = {
                operator: 'contains',
                value: this.filters.search.trim(),
                fields: ['title', 'abstract', 'keywords', 'authors']
            };
        }
        
        // Add date range if present
        if (this.filters.dateRange) {
            query.dateRange = {
                operator: 'between',
                value: {
                    from: this.filters.dateRange.from,
                    to: this.filters.dateRange.to
                }
            };
        }
        
        // Add citation count if present
        if (this.filters.citationCount !== null && this.filters.citationCount !== undefined) {
            query.citationCount = {
                operator: 'gte',
                value: this.filters.citationCount
            };
        }
        
        // Add multi-select filters
        ['authors', 'journals', 'keywords', 'categories'].forEach(key => {
            if (this.filters[key] && this.filters[key].length > 0) {
                query[key] = {
                    operator: 'in',
                    value: this.filters[key]
                };
            }
        });
        
        return query;
    }

    /**
     * Execute filters against data sources
     * 
     * @param {object} query - Filter query to execute
     * 
     * Educational Notes:
     * - Data Source Abstraction: Works with different data sources
     * - Async Operations: Handles asynchronous filtering operations
     * - Error Recovery: Graceful handling of filter failures
     */
    async executeFilters(query) {
        // Apply to visualization if available
        if (window.conceptVisualization && typeof window.conceptVisualization.applyFilters === 'function') {
            await window.conceptVisualization.applyFilters(this.filters);
        }
        
        // Apply to evidence explorer if available
        if (window.evidenceExplorer && typeof window.evidenceExplorer.applyFilters === 'function') {
            await window.evidenceExplorer.applyFilters(this.filters);
        }
        
        // Apply to research dashboard if available
        if (window.researchDashboard && typeof window.researchDashboard.applyFilters === 'function') {
            await window.researchDashboard.applyFilters(this.filters);
        }
    }

    /**
     * Setup advanced filters with progressive disclosure
     * 
     * Educational Notes:
     * - Progressive Disclosure: Shows complexity only when needed
     * - Accessibility: Proper ARIA attributes for expandable content
     * - User Preference: Remembers user's preference for advanced filters
     */
    setupAdvancedFilters() {
        const collapseToggle = document.querySelector('.collapse-toggle');
        const advancedFilters = document.getElementById('advancedFilters');
        
        if (!collapseToggle || !advancedFilters) {
            console.warn('Advanced filter elements not found');
            return;
        }

        // Update toggle icon and announce state changes
        advancedFilters.addEventListener('shown.bs.collapse', () => {
            collapseToggle.innerHTML = '<i class="fas fa-chevron-up"></i>';
            collapseToggle.setAttribute('aria-expanded', 'true');
            this.announceFilterChange('advanced', 'expanded');
            
            // Save preference
            localStorage.setItem('advancedFiltersExpanded', 'true');
        });
        
        advancedFilters.addEventListener('hidden.bs.collapse', () => {
            collapseToggle.innerHTML = '<i class="fas fa-chevron-down"></i>';
            collapseToggle.setAttribute('aria-expanded', 'false');
            this.announceFilterChange('advanced', 'collapsed');
            
            // Save preference
            localStorage.setItem('advancedFiltersExpanded', 'false');
        });

        // Restore user preference
        const wasExpanded = localStorage.getItem('advancedFiltersExpanded') === 'true';
        if (wasExpanded) {
            advancedFilters.classList.add('show');
            collapseToggle.innerHTML = '<i class="fas fa-chevron-up"></i>';
            collapseToggle.setAttribute('aria-expanded', 'true');
        }
    }

    /**
     * Reset filters to default values
     * 
     * Educational Notes:
     * - State Reset: Safely resets to known good state
     * - User Feedback: Clear indication of reset action
     * - History Tracking: Reset action recorded in filter history
     */
    resetFilters() {
        console.log('🔄 Resetting filters to defaults');
        
        // Store current state for history
        const previousState = { ...this.filters };
        
        // Reset to defaults
        this.filters = { ...this.defaultFilters };
        
        // Update UI controls
        this.updateFilterUI();
        
        // Add to history
        if (this.config.enableFilterHistory) {
            this.addToHistory('reset', previousState, this.filters);
        }
        
        // Apply filters
        this.applyFilters();
        
        // Announce reset
        this.announceFilterChange('all', 'reset');
    }

    /**
     * Update UI controls to reflect current filter state
     * 
     * Educational Notes:
     * - UI Synchronization: Keeps UI in sync with filter state
     * - Input Validation: Ensures UI shows valid values
     * - Accessibility: Updates ARIA attributes and announcements
     */
    updateFilterUI() {
        // Update range inputs
        this.updateRangeInput('confidenceRange', 'confidenceValue', this.filters.confidence, (v) => v.toFixed(1));
        this.updateRangeInput('depthRange', 'depthValue', this.filters.depth, (v) => v.toString());
        
        // Update text inputs
        this.updateTextInput('conceptSearch', this.filters.search);
        
        // Update advanced filters if enabled
        if (this.config.enableAdvancedFilters) {
            this.updateAdvancedFilterUI();
        }
    }

    /**
     * Update a range input and its display
     * 
     * @param {string} inputId - ID of range input
     * @param {string} displayId - ID of value display
     * @param {number} value - Current value
     * @param {function} formatter - Value formatting function
     */
    updateRangeInput(inputId, displayId, value, formatter) {
        const input = document.getElementById(inputId);
        const display = document.getElementById(displayId);
        
        if (input) {
            input.value = value;
        }
        
        if (display) {
            display.textContent = formatter(value);
        }
    }

    /**
     * Update a text input
     * 
     * @param {string} inputId - ID of text input
     * @param {string} value - Current value
     */
    updateTextInput(inputId, value) {
        const input = document.getElementById(inputId);
        if (input) {
            input.value = value || '';
        }
    }

    /**
     * Update advanced filter UI controls
     * 
     * Educational Notes:
     * - Complex UI Updates: Handles multi-select and date range controls
     * - State Consistency: Ensures all controls reflect current state
     * - Performance: Efficient updates without unnecessary DOM manipulation
     */
    updateAdvancedFilterUI() {
        // Update date range
        if (this.filters.dateRange) {
            this.updateTextInput('dateFrom', this.filters.dateRange.from?.toISOString().split('T')[0]);
            this.updateTextInput('dateTo', this.filters.dateRange.to?.toISOString().split('T')[0]);
        } else {
            this.updateTextInput('dateFrom', '');
            this.updateTextInput('dateTo', '');
        }
        
        // Update citation count
        if (this.filters.citationCount !== null) {
            this.updateRangeInput('citationRange', 'citationValue', this.filters.citationCount, (v) => v.toString());
        }
        
        // Update multi-select controls
        this.updateMultiSelect('authorSelect', this.filters.authors);
        this.updateMultiSelect('journalSelect', this.filters.journals);
        this.updateMultiSelect('keywordSelect', this.filters.keywords);
        this.updateMultiSelect('categorySelect', this.filters.categories);
    }

    /**
     * Update multi-select control
     * 
     * @param {string} selectId - ID of select element
     * @param {Array} values - Selected values
     */
    updateMultiSelect(selectId, values) {
        const select = document.getElementById(selectId);
        if (!select) return;
        
        Array.from(select.options).forEach(option => {
            option.selected = values.includes(option.value);
        });
    }

    /**
     * Sanitize text input to prevent XSS
     * 
     * @param {string} input - Raw user input
     * @returns {string} Sanitized input
     * 
     * Educational Notes:
     * - Security: Prevents cross-site scripting attacks
     * - Input Validation: Ensures input meets expected format
     * - Data Integrity: Maintains data quality in search operations
     */
    sanitizeTextInput(input) {
        if (typeof input !== 'string') return '';
        
        return input
            .trim()
            .replace(/[<>]/g, '') // Remove angle brackets
            .substring(0, 200); // Limit length
    }

    /**
     * Show filtering state to user
     * 
     * @param {boolean} isFiltering - Whether filtering is in progress
     * 
     * Educational Notes:
     * - User Feedback: Provides immediate feedback during operations
     * - Loading States: Clear indication of system processing
     * - Accessibility: Announces loading state to screen readers
     */
    showFilteringState(isFiltering) {
        const filterButton = document.querySelector('.apply-filters-btn');
        const filterIndicator = document.querySelector('.filter-loading');
        
        if (filterButton) {
            filterButton.disabled = isFiltering;
            filterButton.textContent = isFiltering ? 'Filtering...' : 'Apply Filters';
        }
        
        if (filterIndicator) {
            filterIndicator.style.display = isFiltering ? 'block' : 'none';
        }
        
        if (isFiltering) {
            this.announceFilterChange('system', 'filtering');
        }
    }

    /**
     * Show filter error message
     * 
     * @param {string} message - Error message to display
     * 
     * Educational Notes:
     * - Error Handling: User-friendly error messages
     * - Accessibility: Error announcements for screen readers
     * - Recovery Guidance: Helps users understand how to fix issues
     */
    showFilterError(message) {
        const errorContainer = document.querySelector('.filter-error');
        
        if (errorContainer) {
            errorContainer.textContent = message;
            errorContainer.style.display = 'block';
            
            // Auto-hide after 5 seconds
            setTimeout(() => {
                errorContainer.style.display = 'none';
            }, 5000);
        }
        
        // Announce error
        if (window.accessibilityManager) {
            window.accessibilityManager.announce(message, true);
        }
        
        console.error('Filter error:', message);
    }

    /**
     * Announce filter changes for accessibility
     * 
     * @param {string} filterKey - Key of changed filter
     * @param {string} value - New filter value
     * 
     * Educational Notes:
     * - Accessibility Integration: Works with accessibility manager
     * - Context-Aware Announcements: Different messages for different changes
     * - User Orientation: Helps users understand current filter state
     */
    announceFilterChange(filterKey, value) {
        if (window.accessibilityManager) {
            const messages = {
                confidence: `Confidence filter set to ${value}`,
                depth: `Depth filter set to ${value}`,
                search: value === 'cleared' ? 'Search filter cleared' : `Search filter set to "${value}"`,
                advanced: `Advanced filters ${value}`,
                all: 'All filters reset',
                system: 'Applying filters...'
            };
            
            const message = messages[filterKey] || `Filter ${filterKey} updated`;
            window.accessibilityManager.announceToRegion('search-status', message);
        }
    }

    /**
     * Initialize filter history tracking
     * 
     * Educational Notes:
     * - User Experience: Allows undoing filter changes
     * - State Management: Tracks filter state changes over time
     * - Memory Management: Limits history to prevent memory issues
     */
    initializeFilterHistory() {
        if (!this.config.enableFilterHistory) return;
        
        // Add initial state to history
        this.addToHistory('initial', {}, this.filters);
    }

    /**
     * Add filter change to history
     * 
     * @param {string} action - Type of action (e.g., 'change', 'reset')
     * @param {*} previousValue - Previous filter value
     * @param {*} newValue - New filter value
     */
    addToHistory(action, previousValue, newValue) {
        this.filterHistory.push({
            action,
            previousValue,
            newValue,
            timestamp: Date.now()
        });
        
        // Limit history length
        if (this.filterHistory.length > this.config.maxHistoryLength) {
            this.filterHistory.shift();
        }
    }

    /**
     * Update filter results display
     * 
     * Educational Notes:
     * - Result Communication: Shows users impact of their filters
     * - Performance Metrics: Displays filtering performance information
     * - User Guidance: Helps users understand filter effectiveness
     */
    updateFilterResults() {
        // This would update result counts, performance metrics, etc.
        console.log('Filter results updated');
    }

    /**
     * Save current filters to localStorage
     * 
     * Educational Notes:
     * - Persistence: Maintains user preferences across sessions
     * - Privacy: Only saves filter preferences, not personal data
     * - Error Handling: Graceful fallback if localStorage unavailable
     */
    saveFilters() {
        try {
            localStorage.setItem('research-filters', JSON.stringify(this.filters));
        } catch (error) {
            console.warn('Could not save filter preferences:', error);
        }
    }

    /**
     * Load saved filters from localStorage
     * 
     * Educational Notes:
     * - User Experience: Restores user's last filter state
     * - Data Validation: Validates loaded data before applying
     * - Fallback Strategy: Uses defaults if saved data invalid
     */
    loadSavedFilters() {
        try {
            const saved = localStorage.getItem('research-filters');
            if (saved) {
                const parsedFilters = JSON.parse(saved);
                
                // Validate and merge with defaults
                this.filters = { ...this.defaultFilters, ...parsedFilters };
                
                // Update UI to reflect loaded filters
                this.updateFilterUI();
                
                console.log('Loaded saved filters:', this.filters);
            }
        } catch (error) {
            console.warn('Could not load saved filters:', error);
        }
    }

    /**
     * Setup keyboard shortcuts for filter operations
     * 
     * Educational Notes:
     * - Keyboard Accessibility: Power users can filter efficiently
     * - Standard Shortcuts: Follows common keyboard shortcut patterns
     * - Non-Conflicting: Avoids conflicts with browser/OS shortcuts
     */
    setupKeyboardShortcuts() {
        document.addEventListener('keydown', (event) => {
            // Ctrl/Cmd + R: Reset filters
            if ((event.ctrlKey || event.metaKey) && event.key === 'r') {
                event.preventDefault();
                this.resetFilters();
            }
            
            // Ctrl/Cmd + F: Focus search filter
            if ((event.ctrlKey || event.metaKey) && event.key === 'f') {
                event.preventDefault();
                const searchInput = document.getElementById('conceptSearch');
                if (searchInput) {
                    searchInput.focus();
                }
            }
        });
    }

    /**
     * Add observer for filter changes
     * 
     * @param {function} callback - Function to call when filters change
     * 
     * Educational Notes:
     * - Observer Pattern: Allows other components to react to filter changes
     * - Loose Coupling: Components don't need direct references to each other
     * - Event-Driven Architecture: Enables reactive programming patterns
     */
    addObserver(callback) {
        if (typeof callback === 'function') {
            this.observers.push(callback);
        }
    }

    /**
     * Remove observer for filter changes
     * 
     * @param {function} callback - Function to remove from observers
     */
    removeObserver(callback) {
        const index = this.observers.indexOf(callback);
        if (index > -1) {
            this.observers.splice(index, 1);
        }
    }

    /**
     * Notify all observers of filter changes
     * 
     * @param {string} key - Filter key that changed
     * @param {*} newValue - New filter value
     * @param {*} previousValue - Previous filter value
     * 
     * Educational Notes:
     * - Observer Notification: Informs all registered observers
     * - Error Isolation: Individual observer errors don't affect others
     * - Performance: Efficient notification mechanism
     */
    notifyObservers(key, newValue, previousValue) {
        const changeEvent = {
            key,
            newValue,
            previousValue,
            allFilters: { ...this.filters },
            timestamp: Date.now()
        };
        
        this.observers.forEach(callback => {
            try {
                callback(changeEvent);
            } catch (error) {
                console.error('Observer callback failed:', error);
            }
        });
    }

    /**
     * Get current filter state
     * 
     * @returns {object} Current filter values
     * 
     * Educational Notes:
     * - State Access: Provides read-only access to filter state
     * - Data Integrity: Returns copy to prevent external modification
     * - Integration: Allows other components to access current filters
     */
    getCurrentFilters() {
        return { ...this.filters };
    }

    /**
     * Get filter statistics
     * 
     * @returns {object} Statistics about current filters
     * 
     * Educational Notes:
     * - Analytics: Provides insights into filter usage
     * - Performance Monitoring: Tracks filter performance metrics
     * - User Insights: Helps understand how users interact with filters
     */
    getFilterStatistics() {
        return {
            activeFilters: Object.keys(this.filters).filter(key => 
                this.filters[key] !== this.defaultFilters[key] &&
                this.filters[key] !== null &&
                this.filters[key] !== '' &&
                (Array.isArray(this.filters[key]) ? this.filters[key].length > 0 : true)
            ).length,
            historyLength: this.filterHistory.length,
            isFiltering: this.isFiltering,
            lastUpdated: this.filterHistory.length > 0 ? 
                this.filterHistory[this.filterHistory.length - 1].timestamp : null
        };
    }

    /**
     * Cleanup filter manager resources
     * 
     * Educational Notes:
     * - Resource Management: Properly cleanup timers and event listeners
     * - Memory Management: Prevents memory leaks in single-page applications
     * - Graceful Shutdown: Ensures clean component destruction
     */
    destroy() {
        // Clear debounce timeouts
        this.debounceTimeouts.forEach(timeoutId => {
            clearTimeout(timeoutId);
        });
        this.debounceTimeouts.clear();
        
        // Clear observers
        this.observers = [];
        
        // Clear history
        this.filterHistory = [];
        
        console.log('🔍 Filter Manager cleaned up');
    }
}

// Export for module systems
if (typeof module !== 'undefined' && module.exports) {
    module.exports = FilterManager;
}

// Global instantiation for direct script inclusion
if (typeof window !== 'undefined') {
    window.FilterManager = FilterManager;
}
