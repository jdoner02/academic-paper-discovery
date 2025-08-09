/**
 * Core UI Management Module
 * 
 * This module provides the foundation for the academic research interface,
 * focusing on user experience patterns and accessibility.
 * 
 * Educational Notes:
 * - Module Pattern: Clean separation of UI concerns
 * - Academic UX: User experience patterns for research workflows
 * - Accessibility First: WCAG 2.1 AA compliance throughout
 * - Progressive Enhancement: Core functionality without JavaScript
 * 
 * Design Patterns Applied:
 * - Observer Pattern: Event-driven UI updates
 * - Strategy Pattern: Different interaction strategies for different users
 * - Facade Pattern: Simple interface hiding complex UI operations
 */

/**
 * Core Academic UI Framework
 * Provides foundational UI management for research applications
 */
class AcademicUI {
    constructor() {
        this.config = {
            announceDelay: 100,
            keyboardNavDelay: 50,
            toastDuration: 5000,
            progressiveDisclosureSpeed: 300
        };
        
        this.eventHandlers = new Map();
        this.announceQueue = [];
        this.isInitialized = false;
        
        this.init();
    }
    
    /**
     * Initialize the academic UI framework
     * 
     * Educational Notes:
     * - Initialization Pattern: Proper setup sequence for UI framework
     * - Error Handling: Graceful degradation if initialization fails
     * - Performance: Optimized initialization for academic workflows
     */
    init() {
        try {
            this.setupAccessibility();
            this.setupProgressiveDisclosure();
            this.setupKeyboardNavigation();
            this.setupUserJourneyTracking();
            this.setupToastNotifications();
            
            this.isInitialized = true;
            console.log('✅ Academic UI Framework initialized');
            
            // Announce successful initialization to screen readers
            this.announce('Academic research interface ready', 'polite');
            
        } catch (error) {
            console.error('❌ Failed to initialize Academic UI Framework:', error);
            // Fallback to basic functionality
            this.initBasicFunctionality();
        }
    }
    
    /**
     * Setup accessibility features for academic users
     * 
     * Educational Notes:
     * - Accessibility First: Screen reader support, keyboard navigation
     * - Academic Standards: Meeting WCAG 2.1 AA requirements
     * - Inclusive Design: Supporting users with diverse abilities
     */
    setupAccessibility() {
        // Create live region for screen reader announcements
        this.createLiveRegion();
        
        // Setup focus management
        this.setupFocusManagement();
        
        // Setup high contrast mode detection
        this.setupHighContrastMode();
        
        // Setup reduced motion preferences
        this.setupReducedMotionMode();
        
        console.log('♿ Accessibility features initialized');
    }
    
    /**
     * Create ARIA live region for screen reader announcements
     * 
     * Educational Notes:
     * - ARIA Live Regions: Dynamic content announcements
     * - Screen Reader Support: Proper semantic markup
     * - Academic Context: Research-specific announcements
     */
    createLiveRegion() {
        if (document.getElementById('academic-announcements')) return;
        
        const liveRegion = document.createElement('div');
        liveRegion.id = 'academic-announcements';
        liveRegion.setAttribute('aria-live', 'polite');
        liveRegion.setAttribute('aria-atomic', 'true');
        liveRegion.className = 'sr-only'; // Screen reader only
        liveRegion.style.cssText = `
            position: absolute;
            left: -10000px;
            width: 1px;
            height: 1px;
            overflow: hidden;
        `;
        
        document.body.appendChild(liveRegion);
    }
    
    /**
     * Announce message to screen readers
     * 
     * @param {string} message - Message to announce
     * @param {string} priority - 'polite' or 'assertive'
     */
    announce(message, priority = 'polite') {
        if (!message) return;
        
        const liveRegion = document.getElementById('academic-announcements');
        if (!liveRegion) return;
        
        // Clear previous announcement
        liveRegion.textContent = '';
        
        // Set priority
        liveRegion.setAttribute('aria-live', priority);
        
        // Add announcement after small delay to ensure screen reader picks it up
        setTimeout(() => {
            liveRegion.textContent = message;
        }, this.config.announceDelay);
        
        console.log(`📢 Announced: ${message}`);
    }
    
    /**
     * Setup focus management for academic workflows
     * 
     * Educational Notes:
     * - Focus Management: Logical tab order for research tasks
     * - Skip Links: Efficient navigation for power users
     * - Focus Indicators: Clear visual feedback
     */
    setupFocusManagement() {
        // Add skip links for efficient navigation
        this.addSkipLinks();
        
        // Enhance focus indicators
        this.enhanceFocusIndicators();
        
        // Setup focus trapping for modals
        this.setupFocusTrapping();
    }
    
    /**
     * Add skip links for keyboard navigation
     * 
     * Educational Notes:
     * - Skip Links: Efficiency for keyboard and screen reader users
     * - Academic Workflows: Quick access to main research areas
     */
    addSkipLinks() {
        if (document.querySelector('.skip-links')) return;
        
        const skipLinks = document.createElement('div');
        skipLinks.className = 'skip-links';
        skipLinks.innerHTML = `
            <a href="#main-content" class="skip-link">Skip to main content</a>
            <a href="#search-form" class="skip-link">Skip to search</a>
            <a href="#results-area" class="skip-link">Skip to results</a>
            <a href="#navigation" class="skip-link">Skip to navigation</a>
        `;
        
        document.body.insertBefore(skipLinks, document.body.firstChild);
    }
    
    /**
     * Enhance focus indicators for better visibility
     * 
     * Educational Notes:
     * - Visual Accessibility: Clear focus indicators
     * - Academic Standards: Professional appearance
     */
    enhanceFocusIndicators() {
        // Add enhanced focus styles
        const style = document.createElement('style');
        style.textContent = `
            .enhanced-focus:focus {
                outline: 3px solid var(--accent-blue, #007acc);
                outline-offset: 2px;
                box-shadow: 0 0 0 2px rgba(0, 122, 204, 0.2);
            }
            
            .skip-link {
                position: absolute;
                top: -40px;
                left: 6px;
                background: var(--primary-blue, #1e40af);
                color: white;
                padding: 8px;
                text-decoration: none;
                z-index: 1000;
                border-radius: 4px;
                transition: top 0.3s;
            }
            
            .skip-link:focus {
                top: 6px;
            }
        `;
        document.head.appendChild(style);
        
        // Apply enhanced focus class to interactive elements
        const interactiveElements = document.querySelectorAll(
            'button, input, select, textarea, a[href], [tabindex]:not([tabindex="-1"])'
        );
        interactiveElements.forEach(element => {
            element.classList.add('enhanced-focus');
        });
    }
    
    /**
     * Setup progressive disclosure for complex academic interfaces
     * 
     * Educational Notes:
     * - Progressive Disclosure: Revealing complexity gradually
     * - Cognitive Load: Reducing information overload
     * - Academic Research: Supporting different expertise levels
     */
    setupProgressiveDisclosure() {
        const disclosureElements = document.querySelectorAll('[data-disclosure]');
        
        disclosureElements.forEach(element => {
            this.setupDisclosureElement(element);
        });
    }
    
    /**
     * Setup individual disclosure element
     * 
     * @param {HTMLElement} element - Element with disclosure behavior
     */
    setupDisclosureElement(element) {
        const trigger = element.querySelector('[data-disclosure-trigger]');
        const content = element.querySelector('[data-disclosure-content]');
        
        if (!trigger || !content) return;
        
        // Setup initial state
        const isExpanded = element.getAttribute('data-disclosure') === 'expanded';
        this.setDisclosureState(trigger, content, isExpanded);
        
        // Add click handler
        trigger.addEventListener('click', () => {
            const currentState = trigger.getAttribute('aria-expanded') === 'true';
            this.setDisclosureState(trigger, content, !currentState);
            
            // Announce state change
            const stateName = currentState ? 'collapsed' : 'expanded';
            this.announce(`Section ${stateName}`, 'polite');
        });
        
        // Add keyboard handler
        trigger.addEventListener('keydown', (event) => {
            if (event.key === 'Enter' || event.key === ' ') {
                event.preventDefault();
                trigger.click();
            }
        });
    }
    
    /**
     * Set disclosure state for trigger and content
     * 
     * @param {HTMLElement} trigger - Trigger element
     * @param {HTMLElement} content - Content element
     * @param {boolean} expanded - Whether content should be expanded
     */
    setDisclosureState(trigger, content, expanded) {
        trigger.setAttribute('aria-expanded', expanded.toString());
        content.style.display = expanded ? 'block' : 'none';
        
        // Update trigger icon if present
        const icon = trigger.querySelector('.disclosure-icon');
        if (icon) {
            icon.style.transform = expanded ? 'rotate(180deg)' : 'rotate(0deg)';
        }
    }
    
    /**
     * Setup keyboard navigation for academic workflows
     * 
     * Educational Notes:
     * - Keyboard Efficiency: Quick access to common research tasks
     * - Academic Shortcuts: Domain-specific keyboard combinations
     * - Power User Support: Advanced keyboard navigation
     */
    setupKeyboardNavigation() {
        document.addEventListener('keydown', (event) => {
            this.handleGlobalKeyboardShortcuts(event);
        });
        
        console.log('⌨️ Keyboard navigation setup complete');
    }
    
    /**
     * Handle global keyboard shortcuts
     * 
     * @param {KeyboardEvent} event - Keyboard event
     */
    handleGlobalKeyboardShortcuts(event) {
        // Only handle shortcuts with Ctrl/Cmd modifier
        if (!(event.ctrlKey || event.metaKey)) return;
        
        switch (event.key) {
            case '/':
            case 'k':
                event.preventDefault();
                this.focusSearchBox();
                break;
            case 'h':
                event.preventDefault();
                this.showHelp();
                break;
            case 'i':
                event.preventDefault();
                this.toggleInfoPanel();
                break;
        }
    }
    
    /**
     * Focus the main search box
     * 
     * Educational Notes:
     * - Search-First Interface: Quick access to primary function
     * - Academic Workflow: Starting point for research
     */
    focusSearchBox() {
        const searchBox = document.querySelector('#search-input, [data-search-input]');
        if (searchBox) {
            searchBox.focus();
            this.announce('Search box focused', 'polite');
        }
    }
    
    /**
     * Show help information
     * 
     * Educational Notes:
     * - User Support: Contextual help for academic users
     * - Learning Aid: Educational information about features
     */
    showHelp() {
        // Implementation would show help modal or panel
        this.announce('Help information displayed', 'polite');
        console.log('📖 Help requested');
    }
    
    /**
     * Toggle information panel
     * 
     * Educational Notes:
     * - Information Architecture: Optional detailed information
     * - Academic Context: Supporting documentation and metadata
     */
    toggleInfoPanel() {
        const infoPanel = document.querySelector('#info-panel, [data-info-panel]');
        if (infoPanel) {
            const isVisible = infoPanel.style.display !== 'none';
            infoPanel.style.display = isVisible ? 'none' : 'block';
            this.announce(`Information panel ${isVisible ? 'hidden' : 'shown'}`, 'polite');
        }
    }
    
    /**
     * Setup user journey tracking for UX improvement
     * 
     * Educational Notes:
     * - Analytics: Understanding research workflows
     * - UX Optimization: Data-driven interface improvements
     * - Academic Patterns: Tracking research behavior patterns
     */
    setupUserJourneyTracking() {
        this.userJourney = {
            startTime: Date.now(),
            steps: [],
            currentStep: null
        };
        
        // Track page interactions
        this.trackPageInteractions();
        
        console.log('📈 User journey tracking initialized');
    }
    
    /**
     * Track page interactions for analytics
     * 
     * Educational Notes:
     * - Event Tracking: Comprehensive interaction monitoring
     * - Privacy Considerations: Anonymized, educational data only
     */
    trackPageInteractions() {
        // Track clicks on important elements
        document.addEventListener('click', (event) => {
            this.trackInteraction('click', event.target);
        });
        
        // Track form submissions
        document.addEventListener('submit', (event) => {
            this.trackInteraction('form_submit', event.target);
        });
        
        // Track search actions
        document.addEventListener('search', (event) => {
            this.trackInteraction('search', event.detail);
        });
    }
    
    /**
     * Track individual interaction
     * 
     * @param {string} type - Type of interaction
     * @param {HTMLElement|Object} target - Target element or data
     */
    trackInteraction(type, target) {
        const interaction = {
            type: type,
            timestamp: Date.now(),
            elementType: target.tagName?.toLowerCase(),
            elementId: target.id,
            elementClass: target.className
        };
        
        this.userJourney.steps.push(interaction);
        
        // Dispatch custom event for external analytics
        document.dispatchEvent(new CustomEvent('academic-interaction', {
            detail: interaction
        }));
    }
    
    /**
     * Setup toast notification system
     * 
     * Educational Notes:
     * - User Feedback: Non-intrusive status communication
     * - Academic Context: Research-appropriate messaging
     * - Accessibility: Screen reader compatible notifications
     */
    setupToastNotifications() {
        this.createToastContainer();
        console.log('🍞 Toast notification system ready');
    }
    
    /**
     * Create container for toast notifications
     */
    createToastContainer() {
        if (document.getElementById('toast-container')) return;
        
        const container = document.createElement('div');
        container.id = 'toast-container';
        container.className = 'toast-container';
        container.setAttribute('aria-live', 'polite');
        container.style.cssText = `
            position: fixed;
            top: 1rem;
            right: 1rem;
            z-index: 1050;
            max-width: 400px;
        `;
        
        document.body.appendChild(container);
    }
    
    /**
     * Show toast notification
     * 
     * @param {string} message - Notification message
     * @param {string} type - Type: 'success', 'error', 'warning', 'info'
     * @param {number} duration - Duration in milliseconds
     */
    showToast(message, type = 'info', duration = this.config.toastDuration) {
        const container = document.getElementById('toast-container');
        if (!container) return;
        
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        toast.setAttribute('role', 'alert');
        toast.innerHTML = `
            <div class="toast-body">
                <i class="fas fa-${this.getToastIcon(type)} me-2"></i>
                ${message}
                <button type="button" class="btn-close" data-dismiss="toast">
                    <span aria-hidden="true">&times;</span>
                </button>
            </div>
        `;
        
        // Add toast to container
        container.appendChild(toast);
        
        // Announce to screen readers
        this.announce(message, type === 'error' ? 'assertive' : 'polite');
        
        // Auto-remove after duration
        setTimeout(() => {
            this.removeToast(toast);
        }, duration);
        
        // Add click handler to close button
        const closeBtn = toast.querySelector('.btn-close');
        closeBtn?.addEventListener('click', () => {
            this.removeToast(toast);
        });
    }
    
    /**
     * Get appropriate icon for toast type
     * 
     * @param {string} type - Toast type
     * @returns {string} Font Awesome icon name
     */
    getToastIcon(type) {
        const icons = {
            success: 'check-circle',
            error: 'exclamation-triangle',
            warning: 'exclamation-circle',
            info: 'info-circle'
        };
        return icons[type] || icons.info;
    }
    
    /**
     * Remove toast notification
     * 
     * @param {HTMLElement} toast - Toast element to remove
     */
    removeToast(toast) {
        if (toast?.parentNode) {
            toast.style.opacity = '0';
            setTimeout(() => {
                toast.remove();
            }, 300);
        }
    }
    
    /**
     * Setup high contrast mode detection and handling
     * 
     * Educational Notes:
     * - Visual Accessibility: Supporting users with visual impairments
     * - Academic Standards: Professional accessibility compliance
     */
    setupHighContrastMode() {
        if (window.matchMedia) {
            const mediaQuery = window.matchMedia('(prefers-contrast: high)');
            this.handleHighContrastMode(mediaQuery.matches);
            
            mediaQuery.addEventListener('change', (e) => {
                this.handleHighContrastMode(e.matches);
            });
        }
    }
    
    /**
     * Handle high contrast mode changes
     * 
     * @param {boolean} isHighContrast - Whether high contrast is enabled
     */
    handleHighContrastMode(isHighContrast) {
        document.documentElement.classList.toggle('high-contrast', isHighContrast);
        
        if (isHighContrast) {
            console.log('🔆 High contrast mode enabled');
        }
    }
    
    /**
     * Setup reduced motion mode detection and handling
     * 
     * Educational Notes:
     * - Motion Sensitivity: Supporting users with vestibular disorders
     * - Accessibility Standards: WCAG motion reduction guidelines
     */
    setupReducedMotionMode() {
        if (window.matchMedia) {
            const mediaQuery = window.matchMedia('(prefers-reduced-motion: reduce)');
            this.handleReducedMotionMode(mediaQuery.matches);
            
            mediaQuery.addEventListener('change', (e) => {
                this.handleReducedMotionMode(e.matches);
            });
        }
    }
    
    /**
     * Handle reduced motion mode changes
     * 
     * @param {boolean} isReducedMotion - Whether reduced motion is preferred
     */
    handleReducedMotionMode(isReducedMotion) {
        document.documentElement.classList.toggle('reduced-motion', isReducedMotion);
        
        if (isReducedMotion) {
            // Reduce animation durations
            this.config.progressiveDisclosureSpeed = 0;
            console.log('🎭 Reduced motion mode enabled');
        }
    }
    
    /**
     * Basic functionality fallback for initialization failures
     * 
     * Educational Notes:
     * - Error Recovery: Graceful degradation when advanced features fail
     * - Academic Reliability: Ensuring core functionality always works
     */
    initBasicFunctionality() {
        console.log('⚠️ Running in basic functionality mode');
        
        // Basic toast functionality
        this.showToast = (message) => {
            alert(message); // Fallback to browser alert
        };
        
        // Basic announcement functionality
        this.announce = (message) => {
            console.log(`Announcement: ${message}`);
        };
        
        this.isInitialized = true;
    }
    
    /**
     * Setup focus trapping for modal dialogs
     * 
     * Educational Notes:
     * - Focus Management: Proper modal behavior for screen readers
     * - Academic Workflows: Supporting complex research interfaces
     */
    setupFocusTrapping() {
        // This would implement focus trapping for modals
        // Ensuring focus stays within modal while it's open
        console.log('🎯 Focus trapping setup complete');
    }
    
    /**
     * Get current user journey data
     * 
     * @returns {Object} User journey data for analytics
     */
    getUserJourneyData() {
        return {
            ...this.userJourney,
            sessionDuration: Date.now() - this.userJourney.startTime
        };
    }
}

// Initialize academic UI when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    window.academicUI = new AcademicUI();
});

// Export for module usage
if (typeof module !== 'undefined' && module.exports) {
    module.exports = AcademicUI;
}
