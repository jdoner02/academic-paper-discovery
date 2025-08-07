/**
 * Concept Visualization Framework
 * Advanced D3.js visualizations for academic concept exploration
 * Focus: Interactive exploration, evidence linking, hierarchical navigation
 */

class ConceptVisualization {
    constructor() {
        this.svg = null;
        this.width = 0;
        this.height = 0;
        this.data = null;
        this.currentType = 'sunburst';
        this.currentFilters = {};
        this.selectedConcept = null;
        this.zoomLevel = 1;
        
        // Color schemes for different hierarchy levels
        this.colorSchemes = {
            academic: ['#1e3a8a', '#3b82f6', '#0891b2', '#059669', '#f59e0b'],
            confidence: d3.scaleSequential(d3.interpolateBlues),
            evidence: d3.scaleSequential(d3.interpolateGreens)
        };
        
        this.initialize();
    }
    
    /**
     * Initialize the visualization framework
     */
    initialize() {
        console.log('🎨 Initializing Concept Visualization Framework...');
        
        this.setupSVGContainer();
        this.setupInteractionHandlers();
        this.setupResponsiveResize();
        this.setupAccessibility();
        
        console.log('✅ Concept Visualization Framework ready');
    }
    
    /**
     * Setup main SVG container
     */
    setupSVGContainer() {
        const container = document.getElementById('visualization');
        if (!container) {
            console.error('❌ Visualization container not found');
            return;
        }
        
        // Get container dimensions
        const rect = container.getBoundingClientRect();
        this.width = rect.width;
        this.height = Math.max(600, rect.height);
        
        // Create SVG element
        this.svg = d3.select('#mainVisualization')
            .attr('width', this.width)
            .attr('height', this.height)
            .attr('viewBox', `0 0 ${this.width} ${this.height}`)
            .attr('preserveAspectRatio', 'xMidYMid meet');
        
        // Create main group for zoom/pan
        this.mainGroup = this.svg.append('g')
            .attr('class', 'main-group');
        
        // Setup zoom behavior
        this.zoom = d3.zoom()
            .scaleExtent([0.1, 10])
            .on('zoom', (event) => {
                this.mainGroup.attr('transform', event.transform);
                this.zoomLevel = event.transform.k;
                this.updateZoomControls();
            });
        
        this.svg.call(this.zoom);
        
        console.log(`📏 SVG container: ${this.width}x${this.height}`);
    }
    
    /**
     * Setup interaction handlers
     */
    setupInteractionHandlers() {
        // Zoom controls
        const zoomInBtn = document.getElementById('zoomIn');
        const zoomOutBtn = document.getElementById('zoomOut');
        const centerViewBtn = document.getElementById('centerView');
        const fullscreenBtn = document.getElementById('fullscreen');
        
        if (zoomInBtn) {
            zoomInBtn.addEventListener('click', () => this.zoomIn());
        }
        
        if (zoomOutBtn) {
            zoomOutBtn.addEventListener('click', () => this.zoomOut());
        }
        
        if (centerViewBtn) {
            centerViewBtn.addEventListener('click', () => this.centerView());
        }
        
        if (fullscreenBtn) {
            fullscreenBtn.addEventListener('click', () => this.toggleFullscreen());
        }
    }
    
    /**
     * Setup responsive resizing
     */
    setupResponsiveResize() {
        window.addEventListener('resize', () => {
            this.debounceResize();
        });
    }
    
    /**
     * Debounced resize handler
     */
    debounceResize() {
        clearTimeout(this.resizeTimeout);
        this.resizeTimeout = setTimeout(() => {
            this.handleResize();
        }, 250);
    }
    
    /**
     * Handle container resize
     */
    handleResize() {
        const container = document.getElementById('visualization');
        if (!container || !this.svg) return;
        
        const rect = container.getBoundingClientRect();
        const newWidth = rect.width;
        const newHeight = Math.max(600, rect.height);
        
        if (newWidth !== this.width || newHeight !== this.height) {
            this.width = newWidth;
            this.height = newHeight;
            
            this.svg
                .attr('width', this.width)
                .attr('height', this.height)
                .attr('viewBox', `0 0 ${this.width} ${this.height}`);
            
            // Redraw current visualization
            if (this.data) {
                this.redrawVisualization();
            }
            
            console.log(`📏 Resized to: ${this.width}x${this.height}`);
        }
    }
    
    /**
     * Setup accessibility features for visualizations
     */
    setupAccessibility() {
        // Add keyboard navigation
        this.svg.attr('tabindex', 0)
            .attr('role', 'img')
            .attr('aria-label', 'Interactive concept hierarchy visualization');
        
        // Keyboard event handlers
        this.svg.on('keydown', (event) => {
            this.handleKeyboardNavigation(event);
        });
        
        // Add screen reader descriptions
        this.setupScreenReaderSupport();
    }
    
    /**
     * Setup screen reader support
     */
    setupScreenReaderSupport() {
        const desc = this.svg.append('desc')
            .text('Interactive visualization showing research concept hierarchies. Use tab to navigate between concepts, enter to select, and arrow keys to explore relationships.');
        
        this.svg.attr('aria-describedby', 'viz-description');
    }
    
    /**
     * Handle keyboard navigation
     */
    handleKeyboardNavigation(event) {
        switch (event.key) {
            case 'Tab':
                // Tab navigation is handled by focus management
                break;
            case 'Enter':
            case ' ':
                event.preventDefault();
                if (this.focusedNode) {
                    this.selectConcept(this.focusedNode);
                }
                break;
            case 'ArrowUp':
                event.preventDefault();
                this.navigateToParent();
                break;
            case 'ArrowDown':
                event.preventDefault();
                this.navigateToChild();
                break;
            case 'ArrowLeft':
            case 'ArrowRight':
                event.preventDefault();
                this.navigateToSibling(event.key === 'ArrowRight');
                break;
            case 'Escape':
                event.preventDefault();
                this.clearSelection();
                break;
        }
    }
    
    /**
     * Load and display concept data
     */
    async loadConceptData(domain, visualizationType = 'sunburst') {
        console.log(`📊 Loading concept data for ${domain} (${visualizationType})`);
        
        try {
            // Fetch concept hierarchy data
            const response = await fetch(`/api/domains/${domain}/hierarchy`);
            if (!response.ok) throw new Error('Failed to load concept data');
            
            const data = await response.json();
            this.data = this.preprocessData(data);
            this.currentType = visualizationType;
            
            // Create visualization based on type
            await this.createVisualization(visualizationType);
            
            // Show legend
            this.showLegend();
            
            console.log('✅ Concept visualization loaded successfully');
            
        } catch (error) {
            console.error('❌ Error loading concept data:', error);
            throw error;
        }
    }
    
    /**
     * Preprocess raw data for visualization
     */
    preprocessData(rawData) {
        // Convert flat concept list to hierarchical structure
        const hierarchy = this.buildHierarchy(rawData.concepts || []);
        
        // Add computed properties
        this.addComputedProperties(hierarchy);
        
        return {
            ...rawData,
            hierarchy: hierarchy,
            maxDepth: this.calculateMaxDepth(hierarchy),
            totalConcepts: rawData.concepts?.length || 0
        };
    }
    
    /**
     * Build hierarchical structure from flat concept list
     */
    buildHierarchy(concepts) {
        const root = { id: 'root', name: 'Research Domain', children: [], level: 0 };
        const nodeMap = new Map([['root', root]]);
        
        // Create nodes
        concepts.forEach(concept => {
            const node = {
                id: concept.id || concept.name,
                name: concept.name,
                confidence: concept.confidence || 0.5,
                evidence_count: concept.evidence_sentences?.length || 0,
                evidence_sentences: concept.evidence_sentences || [],
                level: concept.hierarchy_level || 1,
                parent_id: concept.parent_id || 'root',
                children: [],
                size: this.calculateNodeSize(concept)
            };
            nodeMap.set(node.id, node);
        });
        
        // Build parent-child relationships
        concepts.forEach(concept => {
            const node = nodeMap.get(concept.id || concept.name);
            const parent = nodeMap.get(concept.parent_id || 'root');
            
            if (node && parent) {
                parent.children.push(node);
                node.parent = parent;
            }
        });
        
        return root;
    }
    
    /**
     * Calculate node size based on evidence and importance
     */
    calculateNodeSize(concept) {
        const evidenceWeight = (concept.evidence_sentences?.length || 0) * 2;
        const confidenceWeight = (concept.confidence || 0.5) * 10;
        return Math.max(10, evidenceWeight + confidenceWeight);
    }
    
    /**
     * Add computed properties for visualization
     */
    addComputedProperties(root) {
        this.addDescendantCounts(root);
        this.addHierarchyLevels(root, 0);
        this.addColorMapping(root);
    }
    
    /**
     * Add descendant counts for sizing
     */
    addDescendantCounts(node) {
        if (!node.children || node.children.length === 0) {
            node.descendantCount = 1;
            return 1;
        }
        
        let count = 1;
        node.children.forEach(child => {
            count += this.addDescendantCounts(child);
        });
        
        node.descendantCount = count;
        return count;
    }
    
    /**
     * Add hierarchy levels
     */
    addHierarchyLevels(node, level) {
        node.level = level;
        if (node.children) {
            node.children.forEach(child => {
                this.addHierarchyLevels(child, level + 1);
            });
        }
    }
    
    /**
     * Add color mapping based on hierarchy level
     */
    addColorMapping(node) {
        const colors = this.colorSchemes.academic;
        node.color = colors[Math.min(node.level, colors.length - 1)];
        
        if (node.children) {
            node.children.forEach(child => {
                this.addColorMapping(child);
            });
        }
    }
    
    /**
     * Calculate maximum hierarchy depth
     */
    calculateMaxDepth(root) {
        if (!root.children || root.children.length === 0) {
            return 0;
        }
        
        return 1 + Math.max(...root.children.map(child => this.calculateMaxDepth(child)));
    }
    
    /**
     * Create visualization based on type
     */
    async createVisualization(type) {
        // Clear previous visualization
        this.mainGroup.selectAll('*').remove();
        
        switch (type) {
            case 'sunburst':
                await this.createSunburstVisualization();
                break;
            case 'treemap':
                await this.createTreemapVisualization();
                break;
            case 'network':
                await this.createNetworkVisualization();
                break;
            default:
                throw new Error(`Unknown visualization type: ${type}`);
        }
        
        // Add common interaction handlers
        this.addInteractionHandlers();
    }
    
    /**
     * Create sunburst visualization
     */
    async createSunburstVisualization() {
        console.log('🌞 Creating sunburst visualization');
        
        const radius = Math.min(this.width, this.height) / 2 - 10;
        const centerX = this.width / 2;
        const centerY = this.height / 2;
        
        // Create hierarchical layout
        const hierarchyData = d3.hierarchy(this.data.hierarchy)
            .sum(d => d.size || 1)
            .sort((a, b) => b.value - a.value);
        
        // Create partition layout
        const partition = d3.partition()
            .size([2 * Math.PI, radius]);
        
        const partitionData = partition(hierarchyData);
        
        // Create arc generator
        const arc = d3.arc()
            .startAngle(d => d.x0)
            .endAngle(d => d.x1)
            .innerRadius(d => d.y0)
            .outerRadius(d => d.y1);
        
        // Create sunburst group
        const sunburstGroup = this.mainGroup.append('g')
            .attr('class', 'sunburst')
            .attr('transform', `translate(${centerX}, ${centerY})`);
        
        // Create arcs
        const arcs = sunburstGroup.selectAll('path')
            .data(partitionData.descendants())
            .enter()
            .append('path')
            .attr('class', 'concept-arc')
            .attr('d', arc)
            .attr('fill', d => this.getConceptColor(d.data))
            .attr('stroke', '#fff')
            .attr('stroke-width', 1)
            .style('cursor', 'pointer')
            .style('opacity', 0.8);
        
        // Add labels for larger arcs
        const labels = sunburstGroup.selectAll('text')
            .data(partitionData.descendants().filter(d => d.y1 - d.y0 > 20))
            .enter()
            .append('text')
            .attr('class', 'concept-label')
            .attr('transform', d => {
                const angle = (d.x0 + d.x1) / 2;
                const radius = (d.y0 + d.y1) / 2;
                return `rotate(${angle * 180 / Math.PI - 90}) translate(${radius}, 0) ${angle > Math.PI ? 'rotate(180)' : ''}`;
            })
            .attr('dy', '0.35em')
            .attr('text-anchor', d => (d.x0 + d.x1) / 2 > Math.PI ? 'end' : 'start')
            .text(d => d.data.name)
            .style('font-size', d => Math.min(12, (d.y1 - d.y0) / 3) + 'px')
            .style('fill', '#333')
            .style('pointer-events', 'none');
        
        // Store references for interaction
        this.visualizationElements = { arcs, labels };
        
        console.log('✅ Sunburst visualization created');
    }
    
    /**
     * Create treemap visualization
     */
    async createTreemapVisualization() {
        console.log('🗺️ Creating treemap visualization');
        
        // Create hierarchical layout
        const hierarchyData = d3.hierarchy(this.data.hierarchy)
            .sum(d => d.size || 1)
            .sort((a, b) => b.value - a.value);
        
        // Create treemap layout
        const treemap = d3.treemap()
            .size([this.width - 40, this.height - 40])
            .padding(2)
            .round(true);
        
        const treemapData = treemap(hierarchyData);
        
        // Create treemap group
        const treemapGroup = this.mainGroup.append('g')
            .attr('class', 'treemap')
            .attr('transform', 'translate(20, 20)');
        
        // Create rectangles
        const rects = treemapGroup.selectAll('rect')
            .data(treemapData.descendants())
            .enter()
            .append('rect')
            .attr('class', 'concept-rect')
            .attr('x', d => d.x0)
            .attr('y', d => d.y0)
            .attr('width', d => d.x1 - d.x0)
            .attr('height', d => d.y1 - d.y0)
            .attr('fill', d => this.getConceptColor(d.data))
            .attr('stroke', '#fff')
            .attr('stroke-width', 1)
            .style('cursor', 'pointer')
            .style('opacity', 0.8);
        
        // Add labels
        const labels = treemapGroup.selectAll('text')
            .data(treemapData.descendants().filter(d => d.x1 - d.x0 > 50 && d.y1 - d.y0 > 20))
            .enter()
            .append('text')
            .attr('class', 'concept-label')
            .attr('x', d => (d.x0 + d.x1) / 2)
            .attr('y', d => (d.y0 + d.y1) / 2)
            .attr('dy', '0.35em')
            .attr('text-anchor', 'middle')
            .text(d => d.data.name)
            .style('font-size', d => Math.min(14, Math.sqrt((d.x1 - d.x0) * (d.y1 - d.y0)) / 10) + 'px')
            .style('fill', '#333')
            .style('pointer-events', 'none');
        
        // Store references for interaction
        this.visualizationElements = { rects, labels };
        
        console.log('✅ Treemap visualization created');
    }
    
    /**
     * Create network visualization
     */
    async createNetworkVisualization() {
        console.log('🕸️ Creating network visualization');
        
        // Flatten hierarchy for network representation
        const nodes = this.flattenHierarchy(this.data.hierarchy);
        const links = this.createLinks(nodes);
        
        // Create force simulation
        const simulation = d3.forceSimulation(nodes)
            .force('link', d3.forceLink(links).id(d => d.id).distance(80))
            .force('charge', d3.forceManyBody().strength(-300))
            .force('center', d3.forceCenter(this.width / 2, this.height / 2))
            .force('collision', d3.forceCollide().radius(d => Math.sqrt(d.size) + 5));
        
        // Create network group
        const networkGroup = this.mainGroup.append('g')
            .attr('class', 'network');
        
        // Create links
        const linkElements = networkGroup.selectAll('line')
            .data(links)
            .enter()
            .append('line')
            .attr('class', 'concept-link')
            .attr('stroke', '#ccc')
            .attr('stroke-width', 1)
            .style('opacity', 0.6);
        
        // Create nodes
        const nodeElements = networkGroup.selectAll('circle')
            .data(nodes)
            .enter()
            .append('circle')
            .attr('class', 'concept-node')
            .attr('r', d => Math.sqrt(d.size))
            .attr('fill', d => this.getConceptColor(d))
            .attr('stroke', '#fff')
            .attr('stroke-width', 2)
            .style('cursor', 'pointer')
            .call(d3.drag()
                .on('start', (event, d) => this.dragStart(event, d, simulation))
                .on('drag', (event, d) => this.dragging(event, d))
                .on('end', (event, d) => this.dragEnd(event, d, simulation)));
        
        // Add labels
        const labelElements = networkGroup.selectAll('text')
            .data(nodes)
            .enter()
            .append('text')
            .attr('class', 'concept-label')
            .text(d => d.name)
            .style('font-size', '10px')
            .style('fill', '#333')
            .style('text-anchor', 'middle')
            .style('pointer-events', 'none');
        
        // Update positions on simulation tick
        simulation.on('tick', () => {
            linkElements
                .attr('x1', d => d.source.x)
                .attr('y1', d => d.source.y)
                .attr('x2', d => d.target.x)
                .attr('y2', d => d.target.y);
            
            nodeElements
                .attr('cx', d => d.x)
                .attr('cy', d => d.y);
            
            labelElements
                .attr('x', d => d.x)
                .attr('y', d => d.y + 15);
        });
        
        // Store references for interaction
        this.visualizationElements = { nodes: nodeElements, links: linkElements, labels: labelElements };
        this.simulation = simulation;
        
        console.log('✅ Network visualization created');
    }
    
    /**
     * Flatten hierarchy for network representation
     */
    flattenHierarchy(root) {
        const nodes = [];
        
        function traverse(node) {
            nodes.push({
                id: node.id,
                name: node.name,
                level: node.level,
                size: node.size || 10,
                confidence: node.confidence || 0.5,
                evidence_count: node.evidence_count || 0,
                color: node.color
            });
            
            if (node.children) {
                node.children.forEach(traverse);
            }
        }
        
        traverse(root);
        return nodes;
    }
    
    /**
     * Create links between nodes
     */
    createLinks(nodes) {
        const links = [];
        const nodeMap = new Map(nodes.map(n => [n.id, n]));
        
        // Create parent-child links (simplified)
        nodes.forEach(node => {
            if (node.level > 0) {
                // Find parent (simplified - would use actual parent relationships)
                const parentLevel = node.level - 1;
                const potentialParents = nodes.filter(n => n.level === parentLevel);
                
                if (potentialParents.length > 0) {
                    // Link to closest parent (simplified logic)
                    const parent = potentialParents[0];
                    links.push({
                        source: parent.id,
                        target: node.id,
                        strength: 0.8
                    });
                }
            }
        });
        
        return links;
    }
    
    /**
     * Get color for concept based on various criteria
     */
    getConceptColor(concept) {
        if (concept.color) return concept.color;
        
        // Color by hierarchy level
        const colors = this.colorSchemes.academic;
        return colors[Math.min(concept.level || 0, colors.length - 1)];
    }
    
    /**
     * Add interaction handlers to visualization elements
     */
    addInteractionHandlers() {
        // Add hover and click handlers based on visualization type
        if (this.visualizationElements) {
            const elements = this.currentType === 'sunburst' ? this.visualizationElements.arcs :
                           this.currentType === 'treemap' ? this.visualizationElements.rects :
                           this.visualizationElements.nodes;
            
            if (elements) {
                elements
                    .on('mouseover', (event, d) => this.handleMouseOver(event, d))
                    .on('mouseout', (event, d) => this.handleMouseOut(event, d))
                    .on('click', (event, d) => this.handleClick(event, d));
            }
        }
    }
    
    /**
     * Handle mouse over events
     */
    handleMouseOver(event, d) {
        const concept = d.data || d;
        
        // Highlight element
        d3.select(event.target)
            .style('opacity', 1)
            .style('stroke-width', 3);
        
        // Show tooltip
        this.showTooltip(event, concept);
        
        // Announce to screen readers
        if (window.academicUI) {
            window.academicUI.announce(`Hovering over concept: ${concept.name}`);
        }
    }
    
    /**
     * Handle mouse out events
     */
    handleMouseOut(event, d) {
        // Remove highlight
        d3.select(event.target)
            .style('opacity', 0.8)
            .style('stroke-width', this.currentType === 'network' ? 2 : 1);
        
        // Hide tooltip
        this.hideTooltip();
    }
    
    /**
     * Handle click events
     */
    handleClick(event, d) {
        const concept = d.data || d;
        this.selectConcept(concept);
        
        // Update progress to evidence examination
        if (window.academicUI) {
            window.academicUI.updateProgress(3);
        }
    }
    
    /**
     * Select and display concept details
     */
    selectConcept(concept) {
        this.selectedConcept = concept;
        
        console.log('🎯 Selected concept:', concept);
        
        // Show concept details panel
        this.showConceptDetails(concept);
        
        // Highlight in visualization
        this.highlightConcept(concept);
        
        // Announce selection
        if (window.academicUI) {
            window.academicUI.announce(`Selected concept: ${concept.name}. ${concept.evidence_count || 0} evidence sentences available.`);
        }
    }
    
    /**
     * Show concept details in side panel
     */
    showConceptDetails(concept) {
        const detailsCard = document.getElementById('conceptDetails');
        const titleElement = document.getElementById('selectedConceptTitle');
        const confidenceElement = document.getElementById('conceptConfidence');
        const evidenceCountElement = document.getElementById('evidenceCount');
        const levelElement = document.getElementById('conceptLevel');
        const evidenceList = document.getElementById('evidenceList');
        const relatedConcepts = document.getElementById('relatedConcepts');
        
        if (!detailsCard) return;
        
        // Show the panel
        detailsCard.style.display = 'block';
        
        // Update content
        if (titleElement) titleElement.textContent = concept.name || 'Unknown Concept';
        if (confidenceElement) confidenceElement.textContent = ((concept.confidence || 0) * 100).toFixed(1) + '%';
        if (evidenceCountElement) evidenceCountElement.textContent = concept.evidence_count || 0;
        if (levelElement) levelElement.textContent = `Level ${concept.level || 0}`;
        
        // Update evidence list
        if (evidenceList) {
            this.populateEvidenceList(evidenceList, concept.evidence_sentences || []);
        }
        
        // Update related concepts
        if (relatedConcepts) {
            this.populateRelatedConcepts(relatedConcepts, concept);
        }
        
        // Scroll to panel on mobile
        if (window.innerWidth < 768) {
            detailsCard.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    }
    
    /**
     * Populate evidence list
     */
    populateEvidenceList(container, evidenceSentences) {
        container.innerHTML = '';
        
        if (!evidenceSentences || evidenceSentences.length === 0) {
            container.innerHTML = '<p class="text-muted">No evidence sentences available.</p>';
            return;
        }
        
        evidenceSentences.slice(0, 5).forEach((evidence, index) => {
            const evidenceItem = document.createElement('div');
            evidenceItem.className = 'evidence-item';
            evidenceItem.innerHTML = `
                <div class="evidence-content">
                    <p class="evidence-text">"${evidence.sentence || evidence.text || 'Evidence text not available'}"</p>
                    <div class="evidence-metadata">
                        <span class="evidence-source">
                            <i class="fas fa-file-pdf me-1"></i>
                            ${evidence.source_paper || 'Unknown source'}
                        </span>
                        <span class="evidence-confidence">
                            <i class="fas fa-chart-bar me-1"></i>
                            ${((evidence.confidence || 0.5) * 100).toFixed(0)}% confidence
                        </span>
                    </div>
                </div>
            `;
            
            // Add click handler for evidence links
            evidenceItem.addEventListener('click', () => {
                this.openEvidenceSource(evidence);
            });
            
            container.appendChild(evidenceItem);
        });
        
        // Add "show more" if there are additional evidence sentences
        if (evidenceSentences.length > 5) {
            const showMoreBtn = document.createElement('button');
            showMoreBtn.className = 'btn btn-sm btn-outline-primary mt-2';
            showMoreBtn.innerHTML = `<i class="fas fa-plus me-1"></i>Show ${evidenceSentences.length - 5} more`;
            showMoreBtn.onclick = () => {
                // Expand to show all evidence
                this.populateEvidenceList(container, evidenceSentences);
            };
            container.appendChild(showMoreBtn);
        }
    }
    
    /**
     * Populate related concepts
     */
    populateRelatedConcepts(container, concept) {
        container.innerHTML = '';
        
        // Find related concepts (simplified - would use actual relationship data)
        const relatedConcepts = this.findRelatedConcepts(concept);
        
        if (relatedConcepts.length === 0) {
            container.innerHTML = '<p class="text-muted">No related concepts found.</p>';
            return;
        }
        
        relatedConcepts.forEach(related => {
            const relatedItem = document.createElement('div');
            relatedItem.className = 'related-item';
            relatedItem.innerHTML = `
                <div class="related-content">
                    <h6 class="related-name">${related.name}</h6>
                    <p class="related-relationship">${related.relationship}</p>
                </div>
            `;
            
            relatedItem.addEventListener('click', () => {
                this.selectConcept(related);
            });
            
            container.appendChild(relatedItem);
        });
    }
    
    /**
     * Find related concepts (simplified implementation)
     */
    findRelatedConcepts(concept) {
        // This would use actual relationship data in a real implementation
        return [
            { name: 'Parent Concept', relationship: 'Parent in hierarchy' },
            { name: 'Sibling Concept', relationship: 'Same hierarchy level' },
            { name: 'Child Concept', relationship: 'Child in hierarchy' }
        ].slice(0, 3);
    }
    
    /**
     * Open evidence source (PDF link)
     */
    openEvidenceSource(evidence) {
        console.log('📄 Opening evidence source:', evidence);
        
        // In a real implementation, this would open the PDF at the specific page/location
        if (evidence.pdf_url) {
            window.open(evidence.pdf_url, '_blank');
        } else {
            console.log('No PDF URL available for evidence');
        }
    }
    
    /**
     * Zoom controls
     */
    zoomIn() {
        this.svg.transition().duration(300).call(
            this.zoom.scaleBy, 1.5
        );
    }
    
    zoomOut() {
        this.svg.transition().duration(300).call(
            this.zoom.scaleBy, 1 / 1.5
        );
    }
    
    centerView() {
        this.svg.transition().duration(500).call(
            this.zoom.transform,
            d3.zoomIdentity
        );
    }
    
    /**
     * Reset view to initial state
     */
    resetView() {
        this.centerView();
        this.clearSelection();
        this.hideConceptDetails();
    }
    
    /**
     * Clear current selection
     */
    clearSelection() {
        this.selectedConcept = null;
        
        // Remove highlights
        if (this.visualizationElements) {
            Object.values(this.visualizationElements).forEach(elements => {
                if (elements && elements.style) {
                    elements.style('opacity', 0.8)
                           .style('stroke-width', this.currentType === 'network' ? 2 : 1);
                }
            });
        }
    }
    
    /**
     * Hide concept details panel
     */
    hideConceptDetails() {
        const detailsCard = document.getElementById('conceptDetails');
        if (detailsCard) {
            detailsCard.style.display = 'none';
        }
    }
    
    /**
     * Apply filters to current visualization
     */
    applyFilters(filters) {
        this.currentFilters = filters;
        console.log('🔍 Applying visualization filters:', filters);
        
        // Implementation would filter nodes based on confidence, depth, search terms
        // This is a simplified example
        if (this.visualizationElements) {
            // Filter by confidence
            if (filters.confidence !== undefined) {
                this.filterByConfidence(filters.confidence);
            }
            
            // Filter by search term
            if (filters.search) {
                this.filterBySearch(filters.search);
            }
        }
    }
    
    /**
     * Filter by confidence level
     */
    filterByConfidence(minConfidence) {
        // Implementation would hide/show elements based on confidence
        console.log(`🎯 Filtering by confidence >= ${minConfidence}`);
    }
    
    /**
     * Filter by search term
     */
    filterBySearch(searchTerm) {
        // Implementation would highlight/filter elements matching search
        console.log(`🔍 Searching for: ${searchTerm}`);
    }
    
    /**
     * Show legend
     */
    showLegend() {
        const legend = document.getElementById('vizLegend');
        if (!legend) return;
        
        legend.style.display = 'block';
        
        const legendItems = legend.querySelector('.legend-items');
        if (!legendItems) return;
        
        // Create legend items based on visualization type
        const items = this.createLegendItems();
        legendItems.innerHTML = items.map(item => `
            <div class="legend-item">
                <div class="legend-color" style="background-color: ${item.color}"></div>
                <span class="legend-label">${item.label}</span>
            </div>
        `).join('');
    }
    
    /**
     * Create legend items
     */
    createLegendItems() {
        return this.colorSchemes.academic.map((color, index) => ({
            color: color,
            label: `Level ${index + 1}`
        }));
    }
    
    /**
     * Redraw visualization (after resize or data change)
     */
    redrawVisualization() {
        if (this.data && this.currentType) {
            this.createVisualization(this.currentType);
        }
    }
    
    /**
     * Drag handlers for network visualization
     */
    dragStart(event, d, simulation) {
        if (!event.active) simulation.alphaTarget(0.3).restart();
        d.fx = d.x;
        d.fy = d.y;
    }
    
    dragging(event, d) {
        d.fx = event.x;
        d.fy = event.y;
    }
    
    dragEnd(event, d, simulation) {
        if (!event.active) simulation.alphaTarget(0);
        d.fx = null;
        d.fy = null;
    }
    
    /**
     * Tooltip functionality
     */
    showTooltip(event, concept) {
        // Implementation for showing concept tooltip
        console.log('💬 Showing tooltip for:', concept.name);
    }
    
    hideTooltip() {
        // Implementation for hiding tooltip
    }
    
    /**
     * Keyboard navigation helpers
     */
    navigateToParent() {
        // Navigate to parent concept
        console.log('⬆️ Navigate to parent');
    }
    
    navigateToChild() {
        // Navigate to child concept
        console.log('⬇️ Navigate to child');
    }
    
    navigateToSibling(next = true) {
        // Navigate to sibling concept
        console.log(next ? '➡️ Navigate to next sibling' : '⬅️ Navigate to previous sibling');
    }
    
    /**
     * Toggle fullscreen mode
     */
    toggleFullscreen() {
        const container = document.getElementById('visualization');
        if (!container) return;
        
        if (!document.fullscreenElement) {
            container.requestFullscreen().then(() => {
                console.log('📺 Entered fullscreen mode');
            });
        } else {
            document.exitFullscreen().then(() => {
                console.log('📺 Exited fullscreen mode');
            });
        }
    }
    
    /**
     * Update zoom control states
     */
    updateZoomControls() {
        // Update zoom control button states based on current zoom level
        const zoomInBtn = document.getElementById('zoomIn');
        const zoomOutBtn = document.getElementById('zoomOut');
        
        if (zoomInBtn) {
            zoomInBtn.disabled = this.zoomLevel >= 10;
        }
        
        if (zoomOutBtn) {
            zoomOutBtn.disabled = this.zoomLevel <= 0.1;
        }
    }
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    window.conceptVisualization = new ConceptVisualization();
});

// Export for module usage
if (typeof module !== 'undefined' && module.exports) {
    module.exports = ConceptVisualization;
}
