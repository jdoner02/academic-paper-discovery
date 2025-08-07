/**
 * Evidence Explorer Framework
 * Advanced evidence examination and source linking for academic transparency
 * Focus: Traceability, Credibility, Academic Standards
 */

class EvidenceExplorer {
    constructor() {
        this.currentEvidence = null;
        this.evidenceModal = null;
        this.citationFormat = 'APA'; // Default citation format
        this.evidenceHistory = [];
        this.maxHistorySize = 50;
        
        this.initialize();
    }
    
    /**
     * Initialize evidence explorer framework
     */
    initialize() {
        console.log('📚 Initializing Evidence Explorer Framework...');
        
        this.setupEvidenceModal();
        this.setupCitationFormats();
        this.setupEvidenceNavigation();
        this.setupExportFeatures();
        
        console.log('✅ Evidence Explorer Framework ready');
    }
    
    /**
     * Setup evidence examination modal
     */
    setupEvidenceModal() {
        // Create evidence modal HTML
        const modalHTML = `
            <div class="modal fade" id="evidenceModal" tabindex="-1" aria-labelledby="evidenceModalLabel" aria-hidden="true">
                <div class="modal-dialog modal-xl">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title" id="evidenceModalLabel">
                                <i class="fas fa-search me-2"></i>
                                Evidence Examination
                            </h5>
                            <div class="modal-actions">
                                <button type="button" class="btn btn-sm btn-outline-secondary me-2" id="evidenceHistory">
                                    <i class="fas fa-history me-1"></i>History
                                </button>
                                <button type="button" class="btn btn-sm btn-outline-primary me-2" id="exportEvidence">
                                    <i class="fas fa-download me-1"></i>Export
                                </button>
                                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                            </div>
                        </div>
                        <div class="modal-body">
                            <div class="evidence-container">
                                <!-- Evidence source information -->
                                <div class="evidence-source-info">
                                    <div class="row">
                                        <div class="col-md-8">
                                            <h6 class="evidence-paper-title" id="evidencePaperTitle">-</h6>
                                            <p class="evidence-paper-authors" id="evidencePaperAuthors">-</p>
                                            <p class="evidence-paper-journal" id="evidencePaperJournal">-</p>
                                        </div>
                                        <div class="col-md-4 text-end">
                                            <div class="evidence-metadata">
                                                <div class="metadata-badge" id="evidenceConfidenceBadge">
                                                    <i class="fas fa-chart-line me-1"></i>
                                                    <span id="evidenceConfidenceValue">-</span>% Confidence
                                                </div>
                                                <div class="metadata-badge" id="evidencePageBadge">
                                                    <i class="fas fa-file-alt me-1"></i>
                                                    Page <span id="evidencePageNumber">-</span>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                
                                <!-- Evidence sentence display -->
                                <div class="evidence-content">
                                    <div class="evidence-sentence-container">
                                        <h6>Evidence Sentence:</h6>
                                        <blockquote class="evidence-sentence" id="evidenceSentenceText">
                                            Select an evidence sentence to examine it in detail.
                                        </blockquote>
                                    </div>
                                    
                                    <!-- Context sentences -->
                                    <div class="evidence-context" id="evidenceContext" style="display: none;">
                                        <h6>Context (Surrounding Sentences):</h6>
                                        <div class="context-sentences" id="contextSentences">
                                            <!-- Context will be populated dynamically -->
                                        </div>
                                    </div>
                                </div>
                                
                                <!-- Evidence analysis -->
                                <div class="evidence-analysis">
                                    <div class="row">
                                        <div class="col-md-6">
                                            <h6>Extraction Analysis:</h6>
                                            <div class="analysis-item">
                                                <span class="analysis-label">Extraction Method:</span>
                                                <span class="analysis-value" id="extractionMethod">-</span>
                                            </div>
                                            <div class="analysis-item">
                                                <span class="analysis-label">Keywords Matched:</span>
                                                <span class="analysis-value" id="keywordsMatched">-</span>
                                            </div>
                                            <div class="analysis-item">
                                                <span class="analysis-label">Semantic Similarity:</span>
                                                <span class="analysis-value" id="semanticSimilarity">-</span>
                                            </div>
                                        </div>
                                        <div class="col-md-6">
                                            <h6>Quality Metrics:</h6>
                                            <div class="analysis-item">
                                                <span class="analysis-label">Evidence Strength:</span>
                                                <span class="analysis-value" id="evidenceStrength">-</span>
                                            </div>
                                            <div class="analysis-item">
                                                <span class="analysis-label">Context Relevance:</span>
                                                <span class="analysis-value" id="contextRelevance">-</span>
                                            </div>
                                            <div class="analysis-item">
                                                <span class="analysis-label">Citation Count:</span>
                                                <span class="analysis-value" id="citationCount">-</span>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                
                                <!-- Related evidence -->
                                <div class="related-evidence" id="relatedEvidence">
                                    <h6>Related Evidence:</h6>
                                    <div class="related-evidence-list" id="relatedEvidenceList">
                                        <!-- Related evidence will be populated dynamically -->
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="modal-footer">
                            <div class="citation-section">
                                <label for="citationFormat" class="form-label">Citation Format:</label>
                                <select class="form-select form-select-sm d-inline-block w-auto me-2" id="citationFormat">
                                    <option value="APA">APA</option>
                                    <option value="MLA">MLA</option>
                                    <option value="Chicago">Chicago</option>
                                    <option value="Harvard">Harvard</option>
                                </select>
                                <button type="button" class="btn btn-sm btn-outline-secondary" id="copyCitation">
                                    <i class="fas fa-copy me-1"></i>Copy Citation
                                </button>
                            </div>
                            <div class="evidence-actions">
                                <button type="button" class="btn btn-outline-primary" id="openPdfSource">
                                    <i class="fas fa-external-link-alt me-1"></i>Open PDF Source
                                </button>
                                <button type="button" class="btn btn-primary" id="addToReferences">
                                    <i class="fas fa-bookmark me-1"></i>Add to References
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        // Add modal to page
        document.body.insertAdjacentHTML('beforeend', modalHTML);
        
        // Initialize Bootstrap modal
        this.evidenceModal = new bootstrap.Modal(document.getElementById('evidenceModal'));
        
        // Setup modal event handlers
        this.setupModalEventHandlers();
    }
    
    /**
     * Setup modal event handlers
     */
    setupModalEventHandlers() {
        const modal = document.getElementById('evidenceModal');
        if (!modal) return;
        
        // Citation format change
        const citationFormat = document.getElementById('citationFormat');
        if (citationFormat) {
            citationFormat.addEventListener('change', (e) => {
                this.citationFormat = e.target.value;
                this.updateCitation();
            });
        }
        
        // Copy citation button
        const copyCitationBtn = document.getElementById('copyCitation');
        if (copyCitationBtn) {
            copyCitationBtn.addEventListener('click', () => {
                this.copyCitationToClipboard();
            });
        }
        
        // Open PDF source button
        const openPdfBtn = document.getElementById('openPdfSource');
        if (openPdfBtn) {
            openPdfBtn.addEventListener('click', () => {
                this.openPdfSource();
            });
        }
        
        // Add to references button
        const addToReferencesBtn = document.getElementById('addToReferences');
        if (addToReferencesBtn) {
            addToReferencesBtn.addEventListener('click', () => {
                this.addToReferences();
            });
        }
        
        // Evidence history button
        const evidenceHistoryBtn = document.getElementById('evidenceHistory');
        if (evidenceHistoryBtn) {
            evidenceHistoryBtn.addEventListener('click', () => {
                this.showEvidenceHistory();
            });
        }
        
        // Export evidence button
        const exportEvidenceBtn = document.getElementById('exportEvidence');
        if (exportEvidenceBtn) {
            exportEvidenceBtn.addEventListener('click', () => {
                this.exportEvidence();
            });
        }
    }
    
    /**
     * Setup citation format options
     */
    setupCitationFormats() {
        this.citationFormats = {
            APA: this.formatAPACitation.bind(this),
            MLA: this.formatMLACitation.bind(this),
            Chicago: this.formatChicagoCitation.bind(this),
            Harvard: this.formatHarvardCitation.bind(this)
        };
    }
    
    /**
     * Setup evidence navigation
     */
    setupEvidenceNavigation() {
        // Keyboard navigation for evidence modal
        document.addEventListener('keydown', (e) => {
            if (this.evidenceModal && document.getElementById('evidenceModal').classList.contains('show')) {
                this.handleEvidenceKeyNavigation(e);
            }
        });
    }
    
    /**
     * Handle keyboard navigation in evidence modal
     */
    handleEvidenceKeyNavigation(event) {
        switch (event.key) {
            case 'Escape':
                this.evidenceModal.hide();
                break;
            case 'c':
                if (event.ctrlKey || event.metaKey) {
                    event.preventDefault();
                    this.copyCitationToClipboard();
                }
                break;
            case 'o':
                if (event.ctrlKey || event.metaKey) {
                    event.preventDefault();
                    this.openPdfSource();
                }
                break;
            case 'r':
                if (event.ctrlKey || event.metaKey) {
                    event.preventDefault();
                    this.addToReferences();
                }
                break;
        }
    }
    
    /**
     * Setup evidence export features
     */
    setupExportFeatures() {
        this.exportFormats = {
            'text': this.exportAsText.bind(this),
            'json': this.exportAsJSON.bind(this),
            'bibtex': this.exportAsBibTeX.bind(this),
            'csv': this.exportAsCSV.bind(this)
        };
    }
    
    /**
     * Examine evidence in detail
     */
    examineEvidence(evidence, concept = null) {
        console.log('🔍 Examining evidence:', evidence);
        
        this.currentEvidence = evidence;
        
        // Add to history
        this.addToEvidenceHistory(evidence, concept);
        
        // Populate modal content
        this.populateEvidenceModal(evidence, concept);
        
        // Show modal
        this.evidenceModal.show();
        
        // Announce to screen readers
        if (window.academicUI) {
            window.academicUI.announce('Evidence examination modal opened. Use Tab to navigate through evidence details.');
        }
        
        // Load additional context and related evidence
        this.loadEvidenceContext(evidence);
        this.loadRelatedEvidence(evidence, concept);
    }
    
    /**
     * Populate evidence modal with data
     */
    populateEvidenceModal(evidence, concept) {
        // Update paper information
        this.updateElement('evidencePaperTitle', evidence.source_paper?.title || 'Unknown Paper');
        this.updateElement('evidencePaperAuthors', this.formatAuthors(evidence.source_paper?.authors || []));
        this.updateElement('evidencePaperJournal', this.formatJournal(evidence.source_paper));
        
        // Update evidence metadata
        const confidence = Math.round((evidence.confidence || 0.5) * 100);
        this.updateElement('evidenceConfidenceValue', confidence);
        this.updateElement('evidencePageNumber', evidence.page_number || 'Unknown');
        
        // Update confidence badge color
        const confidenceBadge = document.getElementById('evidenceConfidenceBadge');
        if (confidenceBadge) {
            confidenceBadge.className = `metadata-badge confidence-${this.getConfidenceLevel(confidence)}`;
        }
        
        // Update evidence sentence
        this.updateElement('evidenceSentenceText', evidence.sentence || evidence.text || 'Evidence text not available');
        
        // Update extraction analysis
        this.updateElement('extractionMethod', evidence.extraction_method || 'Unknown');
        this.updateElement('keywordsMatched', this.formatKeywords(evidence.keywords_matched || []));
        this.updateElement('semanticSimilarity', this.formatSimilarity(evidence.semantic_similarity));
        
        // Update quality metrics
        this.updateElement('evidenceStrength', this.formatStrength(evidence.evidence_strength));
        this.updateElement('contextRelevance', this.formatRelevance(evidence.context_relevance));
        this.updateElement('citationCount', evidence.source_paper?.citation_count || 'Unknown');
    }
    
    /**
     * Load evidence context (surrounding sentences)
     */
    async loadEvidenceContext(evidence) {
        if (!evidence.context_sentences) {
            return;
        }
        
        const contextContainer = document.getElementById('evidenceContext');
        const contextSentences = document.getElementById('contextSentences');
        
        if (!contextContainer || !contextSentences) return;
        
        // Show context section
        contextContainer.style.display = 'block';
        
        // Populate context sentences
        contextSentences.innerHTML = '';
        
        evidence.context_sentences.forEach((sentence, index) => {
            const sentenceElement = document.createElement('div');
            sentenceElement.className = `context-sentence ${sentence.is_target ? 'target-sentence' : ''}`;
            sentenceElement.innerHTML = `
                <span class="sentence-number">${index + 1}.</span>
                <span class="sentence-text">${sentence.text}</span>
            `;
            contextSentences.appendChild(sentenceElement);
        });
    }
    
    /**
     * Load related evidence
     */
    async loadRelatedEvidence(evidence, concept) {
        console.log('🔗 Loading related evidence...');
        
        try {
            // In a real implementation, this would fetch related evidence from the backend
            const relatedEvidence = await this.fetchRelatedEvidence(evidence, concept);
            
            const relatedContainer = document.getElementById('relatedEvidence');
            const relatedList = document.getElementById('relatedEvidenceList');
            
            if (!relatedContainer || !relatedList) return;
            
            if (relatedEvidence.length === 0) {
                relatedContainer.style.display = 'none';
                return;
            }
            
            relatedContainer.style.display = 'block';
            relatedList.innerHTML = '';
            
            relatedEvidence.forEach(related => {
                const relatedItem = document.createElement('div');
                relatedItem.className = 'related-evidence-item';
                relatedItem.innerHTML = `
                    <div class="related-evidence-content">
                        <p class="related-sentence">"${related.sentence}"</p>
                        <div class="related-metadata">
                            <span class="related-paper">${related.source_paper?.title || 'Unknown'}</span>
                            <span class="related-confidence">${Math.round((related.confidence || 0.5) * 100)}%</span>
                        </div>
                    </div>
                `;
                
                relatedItem.addEventListener('click', () => {
                    this.examineEvidence(related, concept);
                });
                
                relatedList.appendChild(relatedItem);
            });
            
        } catch (error) {
            console.error('❌ Error loading related evidence:', error);
        }
    }
    
    /**
     * Fetch related evidence (placeholder implementation)
     */
    async fetchRelatedEvidence(evidence, concept) {
        // In a real implementation, this would make an API call
        return [
            {
                sentence: "Related evidence sentence from another paper supporting the same concept.",
                confidence: 0.8,
                source_paper: { title: "Related Research Paper" }
            },
            {
                sentence: "Additional supporting evidence from a different perspective.",
                confidence: 0.7,
                source_paper: { title: "Another Supporting Study" }
            }
        ];
    }
    
    /**
     * Add evidence to examination history
     */
    addToEvidenceHistory(evidence, concept) {
        const historyItem = {
            evidence: evidence,
            concept: concept,
            timestamp: new Date(),
            id: Date.now() + Math.random()
        };
        
        this.evidenceHistory.unshift(historyItem);
        
        // Limit history size
        if (this.evidenceHistory.length > this.maxHistorySize) {
            this.evidenceHistory = this.evidenceHistory.slice(0, this.maxHistorySize);
        }
        
        console.log('📝 Added to evidence history:', historyItem);
    }
    
    /**
     * Show evidence examination history
     */
    showEvidenceHistory() {
        const historyModal = this.createHistoryModal();
        historyModal.show();
    }
    
    /**
     * Create evidence history modal
     */
    createHistoryModal() {
        const historyHTML = `
            <div class="modal fade" id="evidenceHistoryModal" tabindex="-1" aria-hidden="true">
                <div class="modal-dialog modal-lg">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title">
                                <i class="fas fa-history me-2"></i>Evidence Examination History
                            </h5>
                            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                        </div>
                        <div class="modal-body">
                            <div class="history-list" id="evidenceHistoryList">
                                ${this.renderEvidenceHistory()}
                            </div>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-outline-danger" id="clearHistory">
                                <i class="fas fa-trash me-1"></i>Clear History
                            </button>
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        // Remove existing history modal
        const existingModal = document.getElementById('evidenceHistoryModal');
        if (existingModal) {
            existingModal.remove();
        }
        
        // Add new modal
        document.body.insertAdjacentHTML('beforeend', historyHTML);
        
        // Setup event handlers
        const clearHistoryBtn = document.getElementById('clearHistory');
        if (clearHistoryBtn) {
            clearHistoryBtn.addEventListener('click', () => {
                this.clearEvidenceHistory();
            });
        }
        
        return new bootstrap.Modal(document.getElementById('evidenceHistoryModal'));
    }
    
    /**
     * Render evidence history list
     */
    renderEvidenceHistory() {
        if (this.evidenceHistory.length === 0) {
            return '<p class="text-muted text-center">No evidence examination history available.</p>';
        }
        
        return this.evidenceHistory.map(item => `
            <div class="history-item" data-history-id="${item.id}">
                <div class="history-content">
                    <h6 class="history-concept">${item.concept?.name || 'Unknown Concept'}</h6>
                    <p class="history-sentence">"${item.evidence.sentence || item.evidence.text || 'Evidence text'}"</p>
                    <div class="history-metadata">
                        <span class="history-paper">${item.evidence.source_paper?.title || 'Unknown Paper'}</span>
                        <span class="history-time">${this.formatHistoryTime(item.timestamp)}</span>
                    </div>
                </div>
                <button class="btn btn-sm btn-outline-primary review-evidence" data-history-id="${item.id}">
                    <i class="fas fa-eye"></i>
                </button>
            </div>
        `).join('');
    }
    
    /**
     * Format history timestamp
     */
    formatHistoryTime(timestamp) {
        const now = new Date();
        const diff = now - timestamp;
        const minutes = Math.floor(diff / 60000);
        
        if (minutes < 1) return 'Just now';
        if (minutes < 60) return `${minutes}m ago`;
        
        const hours = Math.floor(minutes / 60);
        if (hours < 24) return `${hours}h ago`;
        
        const days = Math.floor(hours / 24);
        return `${days}d ago`;
    }
    
    /**
     * Clear evidence history
     */
    clearEvidenceHistory() {
        this.evidenceHistory = [];
        
        // Update history modal if open
        const historyList = document.getElementById('evidenceHistoryList');
        if (historyList) {
            historyList.innerHTML = '<p class="text-muted text-center">Evidence history cleared.</p>';
        }
        
        console.log('🗑️ Evidence history cleared');
    }
    
    /**
     * Update citation based on current format
     */
    updateCitation() {
        if (!this.currentEvidence) return;
        
        const formatter = this.citationFormats[this.citationFormat];
        if (formatter) {
            const citation = formatter(this.currentEvidence);
            console.log(`📖 ${this.citationFormat} Citation:`, citation);
        }
    }
    
    /**
     * Format APA citation
     */
    formatAPACitation(evidence) {
        const paper = evidence.source_paper || {};
        const authors = this.formatAuthorsAPA(paper.authors || []);
        const year = paper.publication_year || 'n.d.';
        const title = paper.title || 'Unknown title';
        const journal = paper.journal || 'Unknown journal';
        
        return `${authors} (${year}). ${title}. ${journal}.`;
    }
    
    /**
     * Format MLA citation
     */
    formatMLACitation(evidence) {
        const paper = evidence.source_paper || {};
        const authors = this.formatAuthorsMLA(paper.authors || []);
        const title = paper.title || 'Unknown title';
        const journal = paper.journal || 'Unknown journal';
        const year = paper.publication_year || 'n.d.';
        
        return `${authors} "${title}" ${journal}, ${year}.`;
    }
    
    /**
     * Format Chicago citation
     */
    formatChicagoCitation(evidence) {
        const paper = evidence.source_paper || {};
        const authors = this.formatAuthorsChicago(paper.authors || []);
        const title = paper.title || 'Unknown title';
        const journal = paper.journal || 'Unknown journal';
        const year = paper.publication_year || 'n.d.';
        
        return `${authors} "${title}" ${journal} (${year}).`;
    }
    
    /**
     * Format Harvard citation
     */
    formatHarvardCitation(evidence) {
        const paper = evidence.source_paper || {};
        const authors = this.formatAuthorsHarvard(paper.authors || []);
        const year = paper.publication_year || 'n.d.';
        const title = paper.title || 'Unknown title';
        const journal = paper.journal || 'Unknown journal';
        
        return `${authors} ${year}, '${title}', ${journal}.`;
    }
    
    /**
     * Copy citation to clipboard
     */
    async copyCitationToClipboard() {
        if (!this.currentEvidence) return;
        
        const formatter = this.citationFormats[this.citationFormat];
        if (!formatter) return;
        
        const citation = formatter(this.currentEvidence);
        
        try {
            await navigator.clipboard.writeText(citation);
            
            // Show success feedback
            this.showToast('Citation copied to clipboard!', 'success');
            
            console.log('📋 Citation copied to clipboard');
            
            if (window.academicUI) {
                window.academicUI.announce('Citation copied to clipboard');
            }
            
        } catch (error) {
            console.error('❌ Failed to copy citation:', error);
            this.showToast('Failed to copy citation', 'error');
        }
    }
    
    /**
     * Open PDF source
     */
    openPdfSource() {
        if (!this.currentEvidence) return;
        
        const paper = this.currentEvidence.source_paper;
        if (!paper) {
            this.showToast('No source paper information available', 'warning');
            return;
        }
        
        // Construct PDF URL (implementation depends on PDF storage system)
        let pdfUrl = paper.pdf_url;
        
        if (!pdfUrl) {
            // Try to construct URL from DOI or other identifiers
            if (paper.doi) {
                pdfUrl = `https://doi.org/${paper.doi}`;
            } else if (paper.arxiv_id) {
                pdfUrl = `https://arxiv.org/pdf/${paper.arxiv_id}.pdf`;
            } else {
                this.showToast('PDF source not available', 'warning');
                return;
            }
        }
        
        // Open PDF with page number if available
        if (this.currentEvidence.page_number) {
            pdfUrl += `#page=${this.currentEvidence.page_number}`;
        }
        
        window.open(pdfUrl, '_blank');
        
        console.log('📄 Opened PDF source:', pdfUrl);
        
        if (window.academicUI) {
            window.academicUI.announce('PDF source opened in new tab');
        }
    }
    
    /**
     * Add evidence to references collection
     */
    addToReferences() {
        if (!this.currentEvidence) return;
        
        const reference = {
            evidence: this.currentEvidence,
            citation: this.citationFormats[this.citationFormat](this.currentEvidence),
            format: this.citationFormat,
            added_at: new Date()
        };
        
        // Store reference (implementation depends on storage system)
        this.storeReference(reference);
        
        this.showToast('Added to references collection', 'success');
        
        console.log('📚 Added to references:', reference);
        
        if (window.academicUI) {
            window.academicUI.announce('Evidence added to references collection');
        }
    }
    
    /**
     * Store reference in local storage or backend
     */
    storeReference(reference) {
        try {
            const references = JSON.parse(localStorage.getItem('evidence_references') || '[]');
            references.push(reference);
            localStorage.setItem('evidence_references', JSON.stringify(references));
        } catch (error) {
            console.error('❌ Failed to store reference:', error);
        }
    }
    
    /**
     * Export evidence in various formats
     */
    exportEvidence() {
        if (!this.currentEvidence) return;
        
        const exportModal = this.createExportModal();
        exportModal.show();
    }
    
    /**
     * Create export modal
     */
    createExportModal() {
        const exportHTML = `
            <div class="modal fade" id="evidenceExportModal" tabindex="-1" aria-hidden="true">
                <div class="modal-dialog">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title">
                                <i class="fas fa-download me-2"></i>Export Evidence
                            </h5>
                            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                        </div>
                        <div class="modal-body">
                            <p>Choose export format for the current evidence:</p>
                            <div class="export-options">
                                <button class="btn btn-outline-primary me-2 mb-2" onclick="evidenceExplorer.exportAsText()">
                                    <i class="fas fa-file-alt me-1"></i>Text
                                </button>
                                <button class="btn btn-outline-primary me-2 mb-2" onclick="evidenceExplorer.exportAsJSON()">
                                    <i class="fas fa-code me-1"></i>JSON
                                </button>
                                <button class="btn btn-outline-primary me-2 mb-2" onclick="evidenceExplorer.exportAsBibTeX()">
                                    <i class="fas fa-quote-right me-1"></i>BibTeX
                                </button>
                                <button class="btn btn-outline-primary me-2 mb-2" onclick="evidenceExplorer.exportAsCSV()">
                                    <i class="fas fa-table me-1"></i>CSV
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        // Remove existing export modal
        const existingModal = document.getElementById('evidenceExportModal');
        if (existingModal) {
            existingModal.remove();
        }
        
        // Add new modal
        document.body.insertAdjacentHTML('beforeend', exportHTML);
        
        return new bootstrap.Modal(document.getElementById('evidenceExportModal'));
    }
    
    /**
     * Export evidence as text
     */
    exportAsText() {
        const evidence = this.currentEvidence;
        if (!evidence) return;
        
        const text = `Evidence Examination Report
Generated: ${new Date().toLocaleDateString()}

Evidence Sentence:
"${evidence.sentence || evidence.text || 'N/A'}"

Source Paper:
${evidence.source_paper?.title || 'Unknown'}
${this.formatAuthors(evidence.source_paper?.authors || [])}
${evidence.source_paper?.journal || 'Unknown Journal'}

Metadata:
- Confidence: ${Math.round((evidence.confidence || 0.5) * 100)}%
- Page: ${evidence.page_number || 'Unknown'}
- Extraction Method: ${evidence.extraction_method || 'Unknown'}

Citation (${this.citationFormat}):
${this.citationFormats[this.citationFormat](evidence)}
`;
        
        this.downloadFile(text, 'evidence-report.txt', 'text/plain');
    }
    
    /**
     * Export evidence as JSON
     */
    exportAsJSON() {
        const evidence = this.currentEvidence;
        if (!evidence) return;
        
        const exportData = {
            evidence: evidence,
            citation: this.citationFormats[this.citationFormat](evidence),
            format: this.citationFormat,
            exported_at: new Date().toISOString()
        };
        
        const json = JSON.stringify(exportData, null, 2);
        this.downloadFile(json, 'evidence-data.json', 'application/json');
    }
    
    /**
     * Export evidence as BibTeX
     */
    exportAsBibTeX() {
        const evidence = this.currentEvidence;
        if (!evidence) return;
        
        const paper = evidence.source_paper || {};
        const bibtex = `@article{${this.generateBibTeXKey(paper)},
  title={${paper.title || 'Unknown Title'}},
  author={${this.formatAuthorsBibTeX(paper.authors || [])}},
  journal={${paper.journal || 'Unknown Journal'}},
  year={${paper.publication_year || 'Unknown'}},
  doi={${paper.doi || 'Unknown'}},
  note={Evidence sentence: "${evidence.sentence || evidence.text || 'N/A'}"}
}`;
        
        this.downloadFile(bibtex, 'evidence.bib', 'text/plain');
    }
    
    /**
     * Export evidence as CSV
     */
    exportAsCSV() {
        const evidence = this.currentEvidence;
        if (!evidence) return;
        
        const paper = evidence.source_paper || {};
        const csv = `"Evidence Sentence","Source Paper","Authors","Journal","Year","Confidence","Page","Method"
"${evidence.sentence || evidence.text || 'N/A'}","${paper.title || 'Unknown'}","${this.formatAuthors(paper.authors || [])}","${paper.journal || 'Unknown'}","${paper.publication_year || 'Unknown'}","${Math.round((evidence.confidence || 0.5) * 100)}%","${evidence.page_number || 'Unknown'}","${evidence.extraction_method || 'Unknown'}"`;
        
        this.downloadFile(csv, 'evidence-data.csv', 'text/csv');
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
        
        // Close export modal
        const exportModal = bootstrap.Modal.getInstance(document.getElementById('evidenceExportModal'));
        if (exportModal) exportModal.hide();
        
        console.log(`📥 Downloaded: ${filename}`);
    }
    
    /**
     * Utility methods for formatting
     */
    updateElement(id, content) {
        const element = document.getElementById(id);
        if (element) {
            element.textContent = content;
        }
    }
    
    formatAuthors(authors) {
        if (!authors || authors.length === 0) return 'Unknown Authors';
        return authors.map(author => `${author.first_name || ''} ${author.last_name || ''}`.trim()).join(', ');
    }
    
    formatAuthorsAPA(authors) {
        if (!authors || authors.length === 0) return 'Unknown Authors';
        return authors.map(author => `${author.last_name || 'Unknown'}, ${(author.first_name || '').charAt(0)}.`).join(', ');
    }
    
    formatAuthorsMLA(authors) {
        if (!authors || authors.length === 0) return 'Unknown Authors';
        if (authors.length === 1) {
            const author = authors[0];
            return `${author.last_name || 'Unknown'}, ${author.first_name || 'Unknown'}`;
        }
        return this.formatAuthorsAPA(authors);
    }
    
    formatAuthorsChicago(authors) {
        return this.formatAuthorsMLA(authors);
    }
    
    formatAuthorsHarvard(authors) {
        return this.formatAuthorsAPA(authors);
    }
    
    formatAuthorsBibTeX(authors) {
        return authors.map(author => `${author.first_name || ''} ${author.last_name || ''}`.trim()).join(' and ');
    }
    
    formatJournal(paper) {
        if (!paper) return 'Unknown Journal';
        
        const parts = [];
        if (paper.journal) parts.push(paper.journal);
        if (paper.volume) parts.push(`Vol. ${paper.volume}`);
        if (paper.issue) parts.push(`No. ${paper.issue}`);
        if (paper.publication_year) parts.push(`(${paper.publication_year})`);
        
        return parts.join(', ') || 'Unknown Journal';
    }
    
    formatKeywords(keywords) {
        if (!keywords || keywords.length === 0) return 'None';
        return keywords.join(', ');
    }
    
    formatSimilarity(similarity) {
        if (similarity === undefined || similarity === null) return 'Unknown';
        return `${Math.round(similarity * 100)}%`;
    }
    
    formatStrength(strength) {
        if (strength === undefined || strength === null) return 'Unknown';
        const levels = ['Very Low', 'Low', 'Medium', 'High', 'Very High'];
        const index = Math.floor(strength * levels.length);
        return levels[Math.min(index, levels.length - 1)] || 'Unknown';
    }
    
    formatRelevance(relevance) {
        return this.formatStrength(relevance);
    }
    
    getConfidenceLevel(confidence) {
        if (confidence >= 80) return 'high';
        if (confidence >= 60) return 'medium';
        return 'low';
    }
    
    generateBibTeXKey(paper) {
        const author = paper.authors?.[0]?.last_name || 'Unknown';
        const year = paper.publication_year || 'Unknown';
        const title = (paper.title || 'Unknown').split(' ')[0];
        return `${author}${year}${title}`.replace(/[^a-zA-Z0-9]/g, '');
    }
    
    /**
     * Show toast notification
     */
    showToast(message, type = 'info') {
        // Create or update toast notification
        const toastContainer = this.getOrCreateToastContainer();
        
        const toast = document.createElement('div');
        toast.className = `toast align-items-center text-white bg-${type === 'error' ? 'danger' : type === 'warning' ? 'warning' : type === 'success' ? 'success' : 'primary'} border-0`;
        toast.setAttribute('role', 'alert');
        toast.innerHTML = `
            <div class="d-flex">
                <div class="toast-body">${message}</div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
        `;
        
        toastContainer.appendChild(toast);
        
        const bsToast = new bootstrap.Toast(toast);
        bsToast.show();
        
        // Remove toast element after it's hidden
        toast.addEventListener('hidden.bs.toast', () => {
            toast.remove();
        });
    }
    
    /**
     * Get or create toast container
     */
    getOrCreateToastContainer() {
        let container = document.getElementById('toastContainer');
        if (!container) {
            container = document.createElement('div');
            container.id = 'toastContainer';
            container.className = 'toast-container position-fixed top-0 end-0 p-3';
            container.style.zIndex = '9999';
            document.body.appendChild(container);
        }
        return container;
    }
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    window.evidenceExplorer = new EvidenceExplorer();
});

// Export for module usage
if (typeof module !== 'undefined' && module.exports) {
    module.exports = EvidenceExplorer;
}
