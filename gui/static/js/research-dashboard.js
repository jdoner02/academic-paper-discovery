/**
 * Research Dashboard Framework
 * Comprehensive dashboard for academic research interface
 * Focus: User Journey, Progress Tracking, Academic Workflows
 */

class ResearchDashboard {
    constructor() {
        this.userSession = {
            startTime: new Date(),
            searchHistory: [],
            conceptsExplored: [],
            evidenceExamined: [],
            currentGoal: null,
            progressMetrics: {}
        };
        
        this.dashboardState = {
            activeTab: 'overview',
            widgets: new Map(),
            notifications: [],
            preferences: this.loadUserPreferences()
        };
        
        this.initialize();
    }
    
    /**
     * Initialize research dashboard
     */
    initialize() {
        console.log('📊 Initializing Research Dashboard...');
        
        this.setupDashboardLayout();
        this.setupWidgets();
        this.setupProgressTracking();
        this.setupNotifications();
        this.setupPreferences();
        this.setupKeyboardShortcuts();
        
        console.log('✅ Research Dashboard ready');
    }
    
    /**
     * Setup dashboard layout and navigation
     */
    setupDashboardLayout() {
        const dashboardHTML = `
            <div class="research-dashboard" id="researchDashboard">
                <!-- Dashboard Header -->
                <div class="dashboard-header">
                    <div class="dashboard-title">
                        <h4>
                            <i class="fas fa-chart-line me-2"></i>
                            Research Dashboard
                        </h4>
                        <div class="session-info">
                            <span class="session-time" id="sessionTime">Session: 0h 0m</span>
                            <span class="separator">•</span>
                            <span class="concepts-count" id="conceptsCount">0 concepts explored</span>
                        </div>
                    </div>
                    
                    <div class="dashboard-controls">
                        <button class="btn btn-sm btn-outline-secondary me-2" id="dashboardSettings">
                            <i class="fas fa-cog"></i>
                            <span class="d-none d-md-inline ms-1">Settings</span>
                        </button>
                        <button class="btn btn-sm btn-outline-primary me-2" id="exportSession">
                            <i class="fas fa-download"></i>
                            <span class="d-none d-md-inline ms-1">Export</span>
                        </button>
                        <button class="btn btn-sm btn-outline-secondary" id="dashboardHelp">
                            <i class="fas fa-question-circle"></i>
                            <span class="d-none d-md-inline ms-1">Help</span>
                        </button>
                    </div>
                </div>
                
                <!-- Dashboard Navigation -->
                <div class="dashboard-nav">
                    <ul class="nav nav-tabs" id="dashboardTabs" role="tablist">
                        <li class="nav-item" role="presentation">
                            <button class="nav-link active" id="overview-tab" data-bs-toggle="tab" data-bs-target="#overview-panel" type="button" role="tab">
                                <i class="fas fa-tachometer-alt me-1"></i>Overview
                            </button>
                        </li>
                        <li class="nav-item" role="presentation">
                            <button class="nav-link" id="search-tab" data-bs-toggle="tab" data-bs-target="#search-panel" type="button" role="tab">
                                <i class="fas fa-search me-1"></i>Search Progress
                            </button>
                        </li>
                        <li class="nav-item" role="presentation">
                            <button class="nav-link" id="concepts-tab" data-bs-toggle="tab" data-bs-target="#concepts-panel" type="button" role="tab">
                                <i class="fas fa-sitemap me-1"></i>Concepts
                            </button>
                        </li>
                        <li class="nav-item" role="presentation">
                            <button class="nav-link" id="evidence-tab" data-bs-toggle="tab" data-bs-target="#evidence-panel" type="button" role="tab">
                                <i class="fas fa-microscope me-1"></i>Evidence
                            </button>
                        </li>
                        <li class="nav-item" role="presentation">
                            <button class="nav-link" id="insights-tab" data-bs-toggle="tab" data-bs-target="#insights-panel" type="button" role="tab">
                                <i class="fas fa-lightbulb me-1"></i>Insights
                            </button>
                        </li>
                    </ul>
                </div>
                
                <!-- Dashboard Content -->
                <div class="dashboard-content">
                    <div class="tab-content" id="dashboardTabContent">
                        <!-- Overview Panel -->
                        <div class="tab-pane fade show active" id="overview-panel" role="tabpanel">
                            <div class="dashboard-widgets">
                                <div class="row">
                                    <div class="col-md-4">
                                        <div class="widget session-summary" id="sessionSummaryWidget">
                                            <!-- Session summary content -->
                                        </div>
                                    </div>
                                    <div class="col-md-4">
                                        <div class="widget recent-activity" id="recentActivityWidget">
                                            <!-- Recent activity content -->
                                        </div>
                                    </div>
                                    <div class="col-md-4">
                                        <div class="widget progress-metrics" id="progressMetricsWidget">
                                            <!-- Progress metrics content -->
                                        </div>
                                    </div>
                                </div>
                                
                                <div class="row mt-4">
                                    <div class="col-md-8">
                                        <div class="widget research-timeline" id="researchTimelineWidget">
                                            <!-- Research timeline content -->
                                        </div>
                                    </div>
                                    <div class="col-md-4">
                                        <div class="widget quick-actions" id="quickActionsWidget">
                                            <!-- Quick actions content -->
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        
                        <!-- Search Progress Panel -->
                        <div class="tab-pane fade" id="search-panel" role="tabpanel">
                            <div class="search-dashboard">
                                <div class="search-stats" id="searchStats">
                                    <!-- Search statistics -->
                                </div>
                                <div class="search-history" id="searchHistory">
                                    <!-- Search history visualization -->
                                </div>
                            </div>
                        </div>
                        
                        <!-- Concepts Panel -->
                        <div class="tab-pane fade" id="concepts-panel" role="tabpanel">
                            <div class="concepts-dashboard">
                                <div class="concept-overview" id="conceptOverview">
                                    <!-- Concept exploration overview -->
                                </div>
                                <div class="concept-relationships" id="conceptRelationships">
                                    <!-- Concept relationship visualization -->
                                </div>
                            </div>
                        </div>
                        
                        <!-- Evidence Panel -->
                        <div class="tab-pane fade" id="evidence-panel" role="tabpanel">
                            <div class="evidence-dashboard">
                                <div class="evidence-summary" id="evidenceSummary">
                                    <!-- Evidence examination summary -->
                                </div>
                                <div class="evidence-quality" id="evidenceQuality">
                                    <!-- Evidence quality analysis -->
                                </div>
                            </div>
                        </div>
                        
                        <!-- Insights Panel -->
                        <div class="tab-pane fade" id="insights-panel" role="tabpanel">
                            <div class="insights-dashboard">
                                <div class="research-insights" id="researchInsights">
                                    <!-- Research insights and patterns -->
                                </div>
                                <div class="recommendations" id="recommendations">
                                    <!-- Research recommendations -->
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                
                <!-- Dashboard Footer -->
                <div class="dashboard-footer">
                    <div class="footer-stats">
                        <span id="sessionDuration">Session: 0h 0m</span>
                        <span class="separator">•</span>
                        <span id="activityCount">0 activities</span>
                        <span class="separator">•</span>
                        <span id="lastSaved">Auto-saved</span>
                    </div>
                </div>
            </div>
        `;
        
        // Find or create dashboard container
        let dashboardContainer = document.getElementById('dashboardContainer');
        if (!dashboardContainer) {
            dashboardContainer = document.createElement('div');
            dashboardContainer.id = 'dashboardContainer';
            dashboardContainer.className = 'dashboard-container';
            
            // Insert after main content or at the beginning
            const mainContent = document.querySelector('.main-content') || document.body;
            mainContent.insertAdjacentElement('afterbegin', dashboardContainer);
        }
        
        dashboardContainer.innerHTML = dashboardHTML;
        
        // Setup tab change handling
        this.setupTabHandlers();
    }
    
    /**
     * Setup tab change handlers
     */
    setupTabHandlers() {
        const tabs = document.querySelectorAll('#dashboardTabs button[data-bs-toggle="tab"]');
        tabs.forEach(tab => {
            tab.addEventListener('shown.bs.tab', (event) => {
                const targetTab = event.target.getAttribute('data-bs-target').replace('#', '').replace('-panel', '');
                this.switchTab(targetTab);
            });
        });
    }
    
    /**
     * Switch dashboard tab
     */
    switchTab(tabName) {
        this.dashboardState.activeTab = tabName;
        
        // Update widgets for the active tab
        switch (tabName) {
            case 'overview':
                this.updateOverviewWidgets();
                break;
            case 'search':
                this.updateSearchDashboard();
                break;
            case 'concepts':
                this.updateConceptsDashboard();
                break;
            case 'evidence':
                this.updateEvidenceDashboard();
                break;
            case 'insights':
                this.updateInsightsDashboard();
                break;
        }
        
        console.log(`📊 Switched to ${tabName} dashboard`);
        
        if (window.academicUI) {
            window.academicUI.announce(`Switched to ${tabName} dashboard view`);
        }
    }
    
    /**
     * Setup dashboard widgets
     */
    setupWidgets() {
        this.widgets = {
            sessionSummary: new SessionSummaryWidget(),
            recentActivity: new RecentActivityWidget(),
            progressMetrics: new ProgressMetricsWidget(),
            researchTimeline: new ResearchTimelineWidget(),
            quickActions: new QuickActionsWidget()
        };
        
        // Initialize widgets
        Object.values(this.widgets).forEach(widget => {
            if (widget.initialize) {
                widget.initialize();
            }
        });
    }
    
    /**
     * Update overview dashboard widgets
     */
    updateOverviewWidgets() {
        this.widgets.sessionSummary.update(this.userSession);
        this.widgets.recentActivity.update(this.userSession);
        this.widgets.progressMetrics.update(this.userSession);
        this.widgets.researchTimeline.update(this.userSession);
        this.widgets.quickActions.update(this.userSession);
    }
    
    /**
     * Update search dashboard
     */
    updateSearchDashboard() {
        const searchStats = document.getElementById('searchStats');
        const searchHistory = document.getElementById('searchHistory');
        
        if (searchStats) {
            searchStats.innerHTML = this.renderSearchStats();
        }
        
        if (searchHistory) {
            searchHistory.innerHTML = this.renderSearchHistory();
        }
    }
    
    /**
     * Update concepts dashboard
     */
    updateConceptsDashboard() {
        const conceptOverview = document.getElementById('conceptOverview');
        const conceptRelationships = document.getElementById('conceptRelationships');
        
        if (conceptOverview) {
            conceptOverview.innerHTML = this.renderConceptOverview();
        }
        
        if (conceptRelationships) {
            conceptRelationships.innerHTML = this.renderConceptRelationships();
        }
    }
    
    /**
     * Update evidence dashboard
     */
    updateEvidenceDashboard() {
        const evidenceSummary = document.getElementById('evidenceSummary');
        const evidenceQuality = document.getElementById('evidenceQuality');
        
        if (evidenceSummary) {
            evidenceSummary.innerHTML = this.renderEvidenceSummary();
        }
        
        if (evidenceQuality) {
            evidenceQuality.innerHTML = this.renderEvidenceQuality();
        }
    }
    
    /**
     * Update insights dashboard
     */
    updateInsightsDashboard() {
        const researchInsights = document.getElementById('researchInsights');
        const recommendations = document.getElementById('recommendations');
        
        if (researchInsights) {
            researchInsights.innerHTML = this.renderResearchInsights();
        }
        
        if (recommendations) {
            recommendations.innerHTML = this.renderRecommendations();
        }
    }
    
    /**
     * Setup progress tracking
     */
    setupProgressTracking() {
        // Track session duration
        this.sessionTimer = setInterval(() => {
            this.updateSessionTime();
        }, 60000); // Update every minute
        
        // Track user activities
        this.setupActivityTracking();
    }
    
    /**
     * Setup activity tracking
     */
    setupActivityTracking() {
        // Track search activities
        document.addEventListener('searchExecuted', (event) => {
            this.trackActivity('search', event.detail);
        });
        
        // Track concept exploration
        document.addEventListener('conceptExplored', (event) => {
            this.trackActivity('concept', event.detail);
        });
        
        // Track evidence examination
        document.addEventListener('evidenceExamined', (event) => {
            this.trackActivity('evidence', event.detail);
        });
        
        // Track visualization interactions
        document.addEventListener('visualizationInteraction', (event) => {
            this.trackActivity('visualization', event.detail);
        });
    }
    
    /**
     * Track user activity
     */
    trackActivity(type, data) {
        const activity = {
            type: type,
            data: data,
            timestamp: new Date(),
            id: Date.now() + Math.random()
        };
        
        // Add to appropriate session tracking
        switch (type) {
            case 'search':
                this.userSession.searchHistory.push(activity);
                break;
            case 'concept':
                this.userSession.conceptsExplored.push(activity);
                break;
            case 'evidence':
                this.userSession.evidenceExamined.push(activity);
                break;
        }
        
        // Update dashboard if currently visible
        if (this.isDashboardVisible()) {
            this.updateCurrentDashboard();
        }
        
        // Auto-save session
        this.autoSaveSession();
        
        console.log(`📈 Activity tracked: ${type}`, activity);
    }
    
    /**
     * Update session time display
     */
    updateSessionTime() {
        const duration = Date.now() - this.userSession.startTime;
        const hours = Math.floor(duration / 3600000);
        const minutes = Math.floor((duration % 3600000) / 60000);
        
        const timeString = `${hours}h ${minutes}m`;
        
        // Update time displays
        const sessionTimeElements = document.querySelectorAll('#sessionTime, #sessionDuration');
        sessionTimeElements.forEach(element => {
            element.textContent = `Session: ${timeString}`;
        });
        
        // Update concepts count
        const conceptsCount = document.getElementById('conceptsCount');
        if (conceptsCount) {
            const count = this.userSession.conceptsExplored.length;
            conceptsCount.textContent = `${count} concept${count !== 1 ? 's' : ''} explored`;
        }
        
        // Update activity count
        const activityCount = document.getElementById('activityCount');
        if (activityCount) {
            const totalActivities = this.userSession.searchHistory.length + 
                                  this.userSession.conceptsExplored.length + 
                                  this.userSession.evidenceExamined.length;
            activityCount.textContent = `${totalActivities} activities`;
        }
    }
    
    /**
     * Check if dashboard is currently visible
     */
    isDashboardVisible() {
        const dashboard = document.getElementById('researchDashboard');
        return dashboard && dashboard.offsetParent !== null;
    }
    
    /**
     * Update current dashboard view
     */
    updateCurrentDashboard() {
        this.switchTab(this.dashboardState.activeTab);
    }
    
    /**
     * Setup notifications system
     */
    setupNotifications() {
        this.notificationQueue = [];
        this.maxNotifications = 5;
        
        // Check for research milestones
        this.setupMilestoneTracking();
    }
    
    /**
     * Setup milestone tracking
     */
    setupMilestoneTracking() {
        // Check milestones every 5 minutes
        setInterval(() => {
            this.checkResearchMilestones();
        }, 300000);
    }
    
    /**
     * Check for research milestones
     */
    checkResearchMilestones() {
        const session = this.userSession;
        
        // First search milestone
        if (session.searchHistory.length === 1) {
            this.showNotification('🎉 First search completed! Great start to your research.', 'success');
        }
        
        // Concept exploration milestone
        if (session.conceptsExplored.length === 5) {
            this.showNotification('📚 You\'ve explored 5 concepts! Consider examining evidence quality.', 'info');
        }
        
        // Evidence examination milestone
        if (session.evidenceExamined.length === 3) {
            this.showNotification('🔬 You\'ve examined multiple evidence sources. Check the insights tab for patterns.', 'info');
        }
        
        // Session duration milestone
        const duration = Date.now() - session.startTime;
        const hours = Math.floor(duration / 3600000);
        
        if (hours === 1) {
            this.showNotification('⏰ You\'ve been researching for an hour! Consider taking a break.', 'warning');
        }
    }
    
    /**
     * Show notification
     */
    showNotification(message, type = 'info') {
        const notification = {
            id: Date.now() + Math.random(),
            message: message,
            type: type,
            timestamp: new Date(),
            read: false
        };
        
        this.dashboardState.notifications.unshift(notification);
        
        // Limit notifications
        if (this.dashboardState.notifications.length > this.maxNotifications) {
            this.dashboardState.notifications = this.dashboardState.notifications.slice(0, this.maxNotifications);
        }
        
        // Show toast notification
        if (window.academicUI && window.academicUI.showToast) {
            window.academicUI.showToast(message, type);
        }
        
        console.log('🔔 Notification:', notification);
    }
    
    /**
     * Setup user preferences
     */
    setupPreferences() {
        this.defaultPreferences = {
            autoSave: true,
            showNotifications: true,
            trackingEnabled: true,
            dashboardPosition: 'top',
            updateInterval: 60000,
            theme: 'academic'
        };
        
        // Apply preferences
        this.applyPreferences();
    }
    
    /**
     * Load user preferences
     */
    loadUserPreferences() {
        try {
            const saved = localStorage.getItem('research_dashboard_preferences');
            return saved ? { ...this.defaultPreferences, ...JSON.parse(saved) } : { ...this.defaultPreferences };
        } catch (error) {
            console.error('❌ Failed to load preferences:', error);
            return { ...this.defaultPreferences };
        }
    }
    
    /**
     * Save user preferences
     */
    saveUserPreferences() {
        try {
            localStorage.setItem('research_dashboard_preferences', JSON.stringify(this.dashboardState.preferences));
        } catch (error) {
            console.error('❌ Failed to save preferences:', error);
        }
    }
    
    /**
     * Apply user preferences
     */
    applyPreferences() {
        const prefs = this.dashboardState.preferences;
        
        // Apply auto-save setting
        if (prefs.autoSave) {
            this.enableAutoSave();
        }
        
        // Apply notification setting
        if (!prefs.showNotifications) {
            this.disableNotifications();
        }
        
        // Apply theme
        this.applyTheme(prefs.theme);
    }
    
    /**
     * Setup keyboard shortcuts
     */
    setupKeyboardShortcuts() {
        document.addEventListener('keydown', (event) => {
            // Only handle shortcuts when dashboard is visible
            if (!this.isDashboardVisible()) return;
            
            // Check for modifier keys
            const isCtrl = event.ctrlKey || event.metaKey;
            const isShift = event.shiftKey;
            
            if (isCtrl && !isShift) {
                switch (event.key) {
                    case '1':
                        event.preventDefault();
                        this.switchToTab('overview');
                        break;
                    case '2':
                        event.preventDefault();
                        this.switchToTab('search');
                        break;
                    case '3':
                        event.preventDefault();
                        this.switchToTab('concepts');
                        break;
                    case '4':
                        event.preventDefault();
                        this.switchToTab('evidence');
                        break;
                    case '5':
                        event.preventDefault();
                        this.switchToTab('insights');
                        break;
                    case 's':
                        event.preventDefault();
                        this.exportSession();
                        break;
                }
            }
        });
    }
    
    /**
     * Switch to specific tab
     */
    switchToTab(tabName) {
        const tabButton = document.getElementById(`${tabName}-tab`);
        if (tabButton) {
            const tab = new bootstrap.Tab(tabButton);
            tab.show();
        }
    }
    
    /**
     * Auto-save session data
     */
    autoSaveSession() {
        if (!this.dashboardState.preferences.autoSave) return;
        
        try {
            const sessionData = {
                userSession: this.userSession,
                dashboardState: this.dashboardState,
                lastSaved: new Date().toISOString()
            };
            
            localStorage.setItem('research_session_data', JSON.stringify(sessionData));
            
            // Update last saved indicator
            const lastSaved = document.getElementById('lastSaved');
            if (lastSaved) {
                lastSaved.textContent = 'Auto-saved';
            }
            
        } catch (error) {
            console.error('❌ Failed to auto-save session:', error);
        }
    }
    
    /**
     * Export session data
     */
    exportSession() {
        const sessionData = {
            session: this.userSession,
            dashboard: this.dashboardState,
            exported_at: new Date().toISOString(),
            version: '1.0'
        };
        
        const filename = `research-session-${new Date().toISOString().split('T')[0]}.json`;
        this.downloadFile(JSON.stringify(sessionData, null, 2), filename, 'application/json');
        
        console.log('📥 Session exported:', filename);
        
        if (window.academicUI) {
            window.academicUI.announce('Research session exported successfully');
        }
    }
    
    /**
     * Download file utility
     */
    downloadFile(content, filename, mimeType) {
        const blob = new Blob([content], { type: mimeType });
        const url = URL.createObjectURL(blob);
        
        const link = document.createElement('a');
        link.href = url;
        link.download = filename;
        document.body.appendChild(link);
        link.click();
        
        document.body.removeChild(link);
        URL.revokeObjectURL(url);
    }
    
    /**
     * Render search statistics
     */
    renderSearchStats() {
        const searches = this.userSession.searchHistory;
        const totalSearches = searches.length;
        const uniqueQueries = new Set(searches.map(s => s.data?.query)).size;
        const averageResults = searches.length > 0 ? 
            Math.round(searches.reduce((sum, s) => sum + (s.data?.resultCount || 0), 0) / searches.length) : 0;
        
        return `
            <div class="stats-grid">
                <div class="stat-item">
                    <div class="stat-value">${totalSearches}</div>
                    <div class="stat-label">Total Searches</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value">${uniqueQueries}</div>
                    <div class="stat-label">Unique Queries</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value">${averageResults}</div>
                    <div class="stat-label">Avg Results</div>
                </div>
            </div>
        `;
    }
    
    /**
     * Render search history
     */
    renderSearchHistory() {
        const searches = this.userSession.searchHistory.slice(0, 10); // Show last 10
        
        if (searches.length === 0) {
            return '<p class="text-muted text-center">No searches performed yet.</p>';
        }
        
        return `
            <div class="search-history-list">
                ${searches.map(search => `
                    <div class="search-history-item">
                        <div class="search-query">${search.data?.query || 'Unknown query'}</div>
                        <div class="search-metadata">
                            <span class="search-time">${this.formatTime(search.timestamp)}</span>
                            <span class="search-results">${search.data?.resultCount || 0} results</span>
                        </div>
                    </div>
                `).join('')}
            </div>
        `;
    }
    
    /**
     * Render concept overview
     */
    renderConceptOverview() {
        const concepts = this.userSession.conceptsExplored;
        const totalConcepts = concepts.length;
        const recentConcepts = concepts.slice(-5);
        
        return `
            <div class="concept-stats">
                <h6>Concept Exploration Overview</h6>
                <p>You've explored <strong>${totalConcepts}</strong> concepts in this session.</p>
                
                ${recentConcepts.length > 0 ? `
                    <div class="recent-concepts">
                        <h6>Recently Explored:</h6>
                        <div class="concept-list">
                            ${recentConcepts.map(concept => `
                                <div class="concept-item">
                                    <span class="concept-name">${concept.data?.name || 'Unknown'}</span>
                                    <span class="concept-time">${this.formatTime(concept.timestamp)}</span>
                                </div>
                            `).join('')}
                        </div>
                    </div>
                ` : ''}
            </div>
        `;
    }
    
    /**
     * Render concept relationships
     */
    renderConceptRelationships() {
        return `
            <div class="concept-relationships">
                <h6>Concept Relationships</h6>
                <p>Concept relationship visualization would be rendered here using D3.js</p>
                <div id="conceptRelationshipChart" style="height: 300px; border: 1px dashed #ccc; display: flex; align-items: center; justify-content: center;">
                    <span class="text-muted">Relationship Chart Placeholder</span>
                </div>
            </div>
        `;
    }
    
    /**
     * Render evidence summary
     */
    renderEvidenceSummary() {
        const evidence = this.userSession.evidenceExamined;
        const totalEvidence = evidence.length;
        const avgConfidence = evidence.length > 0 ? 
            Math.round(evidence.reduce((sum, e) => sum + (e.data?.confidence || 0.5), 0) / evidence.length * 100) : 0;
        
        return `
            <div class="evidence-stats">
                <h6>Evidence Examination Summary</h6>
                <div class="stats-grid">
                    <div class="stat-item">
                        <div class="stat-value">${totalEvidence}</div>
                        <div class="stat-label">Evidence Examined</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-value">${avgConfidence}%</div>
                        <div class="stat-label">Avg Confidence</div>
                    </div>
                </div>
            </div>
        `;
    }
    
    /**
     * Render evidence quality analysis
     */
    renderEvidenceQuality() {
        return `
            <div class="evidence-quality">
                <h6>Evidence Quality Analysis</h6>
                <p>Quality metrics and patterns would be displayed here</p>
                <div id="evidenceQualityChart" style="height: 200px; border: 1px dashed #ccc; display: flex; align-items: center; justify-content: center;">
                    <span class="text-muted">Quality Chart Placeholder</span>
                </div>
            </div>
        `;
    }
    
    /**
     * Render research insights
     */
    renderResearchInsights() {
        return `
            <div class="research-insights">
                <h6>Research Insights</h6>
                <p>AI-generated insights based on your research patterns would appear here</p>
                <div class="insight-placeholder">
                    <i class="fas fa-lightbulb text-muted" style="font-size: 2rem;"></i>
                    <p class="text-muted">Continue exploring to generate insights</p>
                </div>
            </div>
        `;
    }
    
    /**
     * Render recommendations
     */
    renderRecommendations() {
        return `
            <div class="recommendations">
                <h6>Research Recommendations</h6>
                <p>Personalized recommendations based on your research behavior</p>
                <div class="recommendation-placeholder">
                    <i class="fas fa-compass text-muted" style="font-size: 2rem;"></i>
                    <p class="text-muted">More recommendations will appear as you research</p>
                </div>
            </div>
        `;
    }
    
    /**
     * Format timestamp for display
     */
    formatTime(timestamp) {
        const now = new Date();
        const diff = now - timestamp;
        const minutes = Math.floor(diff / 60000);
        
        if (minutes < 1) return 'Just now';
        if (minutes < 60) return `${minutes}m ago`;
        
        const hours = Math.floor(minutes / 60);
        if (hours < 24) return `${hours}h ago`;
        
        return timestamp.toLocaleDateString();
    }
    
    /**
     * Enable auto-save functionality
     */
    enableAutoSave() {
        if (this.autoSaveInterval) return;
        
        this.autoSaveInterval = setInterval(() => {
            this.autoSaveSession();
        }, this.dashboardState.preferences.updateInterval);
    }
    
    /**
     * Disable notifications
     */
    disableNotifications() {
        this.dashboardState.showNotifications = false;
    }
    
    /**
     * Apply theme
     */
    applyTheme(themeName) {
        const dashboard = document.getElementById('researchDashboard');
        if (dashboard) {
            dashboard.className = `research-dashboard theme-${themeName}`;
        }
    }
    
    /**
     * Clean up resources
     */
    destroy() {
        if (this.sessionTimer) {
            clearInterval(this.sessionTimer);
        }
        
        if (this.autoSaveInterval) {
            clearInterval(this.autoSaveInterval);
        }
        
        // Save final session state
        this.autoSaveSession();
        
        console.log('📊 Research Dashboard destroyed');
    }
}

/**
 * Dashboard Widget Base Class
 */
class DashboardWidget {
    constructor(containerId) {
        this.containerId = containerId;
        this.data = null;
    }
    
    initialize() {
        // Override in subclasses
    }
    
    update(data) {
        this.data = data;
        this.render();
    }
    
    render() {
        // Override in subclasses
    }
}

/**
 * Session Summary Widget
 */
class SessionSummaryWidget extends DashboardWidget {
    render() {
        const container = document.getElementById('sessionSummaryWidget');
        if (!container || !this.data) return;
        
        const duration = Date.now() - this.data.startTime;
        const hours = Math.floor(duration / 3600000);
        const minutes = Math.floor((duration % 3600000) / 60000);
        
        container.innerHTML = `
            <div class="widget-header">
                <h6><i class="fas fa-clock me-2"></i>Session Summary</h6>
            </div>
            <div class="widget-content">
                <div class="session-stat">
                    <span class="stat-value">${hours}h ${minutes}m</span>
                    <span class="stat-label">Duration</span>
                </div>
                <div class="session-stat">
                    <span class="stat-value">${this.data.searchHistory.length}</span>
                    <span class="stat-label">Searches</span>
                </div>
                <div class="session-stat">
                    <span class="stat-value">${this.data.conceptsExplored.length}</span>
                    <span class="stat-label">Concepts</span>
                </div>
                <div class="session-stat">
                    <span class="stat-value">${this.data.evidenceExamined.length}</span>
                    <span class="stat-label">Evidence</span>
                </div>
            </div>
        `;
    }
}

/**
 * Recent Activity Widget
 */
class RecentActivityWidget extends DashboardWidget {
    render() {
        const container = document.getElementById('recentActivityWidget');
        if (!container || !this.data) return;
        
        const allActivities = [
            ...this.data.searchHistory.map(a => ({ ...a, type: 'search' })),
            ...this.data.conceptsExplored.map(a => ({ ...a, type: 'concept' })),
            ...this.data.evidenceExamined.map(a => ({ ...a, type: 'evidence' }))
        ].sort((a, b) => b.timestamp - a.timestamp).slice(0, 5);
        
        container.innerHTML = `
            <div class="widget-header">
                <h6><i class="fas fa-history me-2"></i>Recent Activity</h6>
            </div>
            <div class="widget-content">
                ${allActivities.length > 0 ? `
                    <div class="activity-list">
                        ${allActivities.map(activity => `
                            <div class="activity-item">
                                <i class="fas fa-${this.getActivityIcon(activity.type)} activity-icon"></i>
                                <div class="activity-content">
                                    <div class="activity-text">${this.getActivityText(activity)}</div>
                                    <div class="activity-time">${this.formatTime(activity.timestamp)}</div>
                                </div>
                            </div>
                        `).join('')}
                    </div>
                ` : `
                    <p class="text-muted text-center">No recent activity</p>
                `}
            </div>
        `;
    }
    
    getActivityIcon(type) {
        const icons = {
            search: 'search',
            concept: 'sitemap',
            evidence: 'microscope'
        };
        return icons[type] || 'circle';
    }
    
    getActivityText(activity) {
        switch (activity.type) {
            case 'search':
                return `Searched: "${activity.data?.query || 'Unknown'}"`;
            case 'concept':
                return `Explored: ${activity.data?.name || 'Unknown concept'}`;
            case 'evidence':
                return `Examined evidence from ${activity.data?.source || 'Unknown source'}`;
            default:
                return 'Unknown activity';
        }
    }
    
    formatTime(timestamp) {
        const now = new Date();
        const diff = now - timestamp;
        const minutes = Math.floor(diff / 60000);
        
        if (minutes < 1) return 'Just now';
        if (minutes < 60) return `${minutes}m ago`;
        
        const hours = Math.floor(minutes / 60);
        return `${hours}h ago`;
    }
}

/**
 * Progress Metrics Widget
 */
class ProgressMetricsWidget extends DashboardWidget {
    render() {
        const container = document.getElementById('progressMetricsWidget');
        if (!container || !this.data) return;
        
        const totalActivities = this.data.searchHistory.length + 
                              this.data.conceptsExplored.length + 
                              this.data.evidenceExamined.length;
        
        const researchProgress = Math.min(100, totalActivities * 10); // Rough progress metric
        
        container.innerHTML = `
            <div class="widget-header">
                <h6><i class="fas fa-chart-line me-2"></i>Progress Metrics</h6>
            </div>
            <div class="widget-content">
                <div class="progress-item">
                    <div class="progress-label">Research Progress</div>
                    <div class="progress">
                        <div class="progress-bar" style="width: ${researchProgress}%"></div>
                    </div>
                    <div class="progress-value">${researchProgress}%</div>
                </div>
                
                <div class="metric-grid">
                    <div class="metric-item">
                        <span class="metric-value">${totalActivities}</span>
                        <span class="metric-label">Total Actions</span>
                    </div>
                    <div class="metric-item">
                        <span class="metric-value">${this.data.searchHistory.length > 0 ? 'Active' : 'Starting'}</span>
                        <span class="metric-label">Status</span>
                    </div>
                </div>
            </div>
        `;
    }
}

/**
 * Research Timeline Widget
 */
class ResearchTimelineWidget extends DashboardWidget {
    render() {
        const container = document.getElementById('researchTimelineWidget');
        if (!container || !this.data) return;
        
        container.innerHTML = `
            <div class="widget-header">
                <h6><i class="fas fa-timeline me-2"></i>Research Timeline</h6>
            </div>
            <div class="widget-content">
                <div id="researchTimelineChart" style="height: 200px; border: 1px dashed #ccc; display: flex; align-items: center; justify-content: center;">
                    <span class="text-muted">Timeline visualization would be rendered here</span>
                </div>
            </div>
        `;
    }
}

/**
 * Quick Actions Widget
 */
class QuickActionsWidget extends DashboardWidget {
    render() {
        const container = document.getElementById('quickActionsWidget');
        if (!container) return;
        
        container.innerHTML = `
            <div class="widget-header">
                <h6><i class="fas fa-bolt me-2"></i>Quick Actions</h6>
            </div>
            <div class="widget-content">
                <div class="quick-actions-grid">
                    <button class="btn btn-outline-primary btn-sm mb-2" onclick="window.location.reload()">
                        <i class="fas fa-search me-1"></i>New Search
                    </button>
                    <button class="btn btn-outline-secondary btn-sm mb-2" onclick="researchDashboard.exportSession()">
                        <i class="fas fa-download me-1"></i>Export Session
                    </button>
                    <button class="btn btn-outline-info btn-sm mb-2" onclick="window.print()">
                        <i class="fas fa-print me-1"></i>Print Report
                    </button>
                    <button class="btn btn-outline-success btn-sm mb-2" onclick="researchDashboard.autoSaveSession()">
                        <i class="fas fa-save me-1"></i>Save Progress
                    </button>
                </div>
            </div>
        `;
    }
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    window.researchDashboard = new ResearchDashboard();
});

// Export for module usage
if (typeof module !== 'undefined' && module.exports) {
    module.exports = ResearchDashboard;
}
