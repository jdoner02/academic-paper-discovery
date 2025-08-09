/**
 * Advanced Shape Utilities for D3.js - Cutting-Edge Geometric Morphing
 * 
 * This module implements state-of-the-art shape generation and morphing techniques
 * inspired by the latest Observable notebooks and D3.js community innovations.
 * 
 * Educational Notes:
 * - Demonstrates advanced SVG path generation and manipulation
 * - Shows geometric interpolation mathematics in action
 * - Implements Bézier curve-based shape morphing
 * - Showcases computational geometry principles
 * - Uses latest D3.js v7+ shape manipulation patterns
 * 
 * Mathematical Foundations:
 * - SVG path data format and coordinate systems
 * - Polar coordinate transformations for star shapes
 * - Bézier curve interpolation for smooth morphing
 * - Geometric centroid calculations for shape alignment
 * 
 * Observable Notebook Inspirations:
 * - "Shape Morphing with Path Interpolation" by Mike Bostock
 * - "Custom SVG Symbols" by Philippe Rivière
 * - "Animated Shape Transitions" by D3.js community
 * 
 * Use Cases:
 * - Research concept visualization with domain-specific shapes
 * - Interactive shape exploration for educational purposes
 * - Smooth animated transitions between visualization modes
 * - Academic icon representation for different research fields
 */

import * as d3 from 'd3';

// Enhanced type definitions for shape morphing
export interface ShapeConfig {
  radius: number;
  strokeWidth: number;
  fillOpacity: number;
  points?: number; // For star shapes
  corners?: number; // For polygon shapes
  type: ShapeType;
}

export type ShapeType = 'circle' | 'square' | 'star' | 'hexagon' | 'triangle' | 'academic' | 'diamond';

export interface MorphConfig {
  duration: number;
  easing: (t: number) => number;
  stagger: number;
  interpolationSamples: number;
}

/**
 * Advanced Shape Generator Class
 * Implements cutting-edge shape generation techniques from Observable notebooks
 */
export class AdvancedShapeGenerator {
  
  /**
   * Generate SVG path for circle using parametric equations
   * Educational: Demonstrates polar coordinate mathematics
   */
  static generateCirclePath(radius: number): string {
    // Using parametric circle equation: x = r*cos(θ), y = r*sin(θ)
    return `M ${-radius} 0 A ${radius} ${radius} 0 1 1 ${radius} 0 A ${radius} ${radius} 0 1 1 ${-radius} 0`;
  }

  /**
   * Generate SVG path for square with rounded corners
   * Educational: Shows coordinate system transformations
   */
  static generateSquarePath(size: number, cornerRadius: number = 0): string {
    const half = size / 2;
    
    if (cornerRadius === 0) {
      // Sharp corners - basic rectangle path
      return `M ${-half} ${-half} L ${half} ${-half} L ${half} ${half} L ${-half} ${half} Z`;
    } else {
      // Rounded corners using arc commands
      const r = Math.min(cornerRadius, half / 2);
      return `
        M ${-half + r} ${-half}
        L ${half - r} ${-half}
        Q ${half} ${-half} ${half} ${-half + r}
        L ${half} ${half - r}
        Q ${half} ${half} ${half - r} ${half}
        L ${-half + r} ${half}
        Q ${-half} ${half} ${-half} ${half - r}
        L ${-half} ${-half + r}
        Q ${-half} ${-half} ${-half + r} ${-half}
        Z
      `.replace(/\s+/g, ' ').trim();
    }
  }

  /**
   * Generate SVG path for star shape using polar mathematics
   * Educational: Demonstrates trigonometry and polar coordinate systems
   */
  static generateStarPath(outerRadius: number, points: number = 5, innerRadiusRatio: number = 0.4): string {
    const innerRadius = outerRadius * innerRadiusRatio;
    const angleStep = Math.PI / points; // Half the angle between points
    let path = '';

    for (let i = 0; i < points * 2; i++) {
      const angle = i * angleStep - Math.PI / 2; // Start from top
      const radius = i % 2 === 0 ? outerRadius : innerRadius;
      const x = Math.cos(angle) * radius;
      const y = Math.sin(angle) * radius;
      
      if (i === 0) {
        path += `M ${x.toFixed(3)} ${y.toFixed(3)}`;
      } else {
        path += ` L ${x.toFixed(3)} ${y.toFixed(3)}`;
      }
    }
    
    return path + ' Z';
  }

  /**
   * Generate SVG path for regular polygon
   * Educational: Shows how to create any n-sided regular polygon
   */
  static generatePolygonPath(radius: number, sides: number): string {
    const angleStep = (2 * Math.PI) / sides;
    let path = '';

    for (let i = 0; i < sides; i++) {
      const angle = i * angleStep - Math.PI / 2; // Start from top
      const x = Math.cos(angle) * radius;
      const y = Math.sin(angle) * radius;
      
      if (i === 0) {
        path += `M ${x.toFixed(3)} ${y.toFixed(3)}`;
      } else {
        path += ` L ${x.toFixed(3)} ${y.toFixed(3)}`;
      }
    }
    
    return path + ' Z';
  }

  /**
   * Generate SVG path for academic research icons
   * Educational: Demonstrates domain-specific shape design
   */
  static generateAcademicIcon(domain: string, radius: number): string {
    switch (domain.toLowerCase()) {
      case 'ai_driven_cyber_defense':
      case 'artificial_intelligence_security':
        // Brain-like neural network icon
        return this.generateNeuralNetworkIcon(radius);
      
      case 'post_quantum_cryptography_implementation':
      case 'quantum_cryptanalysis_threats':
        // Quantum-inspired infinity symbol
        return this.generateQuantumIcon(radius);
      
      case 'healthcare_privacy_compliance':
      case 'medical_device_cybersecurity':
        // Medical cross icon
        return this.generateMedicalIcon(radius);
      
      case 'water_infrastructure_incident_response':
      case 'water_treatment_scada_security':
        // Water drop icon
        return this.generateWaterIcon(radius);
      
      case 'industrial_iot_security':
      case 'iot_device_authentication_security':
        // Connected devices icon
        return this.generateIoTIcon(radius);
      
      default:
        // Default academic icon (graduation cap)
        return this.generateDefaultAcademicIcon(radius);
    }
  }

  /**
   * Generate neural network brain icon
   * Educational: Shows how to create complex shapes from basic geometry
   */
  private static generateNeuralNetworkIcon(radius: number): string {
    const r = radius * 0.8;
    // Create brain-like shape with interconnected nodes
    return `
      M ${-r * 0.6} ${-r * 0.4}
      Q ${-r * 0.8} ${-r * 0.8} ${-r * 0.2} ${-r * 0.6}
      Q ${r * 0.2} ${-r * 0.8} ${r * 0.6} ${-r * 0.4}
      Q ${r * 0.8} ${-r * 0.2} ${r * 0.6} ${r * 0.2}
      Q ${r * 0.4} ${r * 0.6} ${0} ${r * 0.4}
      Q ${-r * 0.4} ${r * 0.6} ${-r * 0.6} ${r * 0.2}
      Q ${-r * 0.8} ${-r * 0.2} ${-r * 0.6} ${-r * 0.4}
      Z
    `.replace(/\s+/g, ' ').trim();
  }

  /**
   * Generate quantum infinity symbol
   * Educational: Demonstrates Bézier curve mathematics
   */
  private static generateQuantumIcon(radius: number): string {
    const r = radius * 0.6;
    // Infinity symbol using Bézier curves
    return `
      M ${-r} 0
      C ${-r} ${-r * 0.6} ${-r * 0.3} ${-r * 0.6} 0 0
      C ${r * 0.3} ${r * 0.6} ${r} ${r * 0.6} ${r} 0
      C ${r} ${-r * 0.6} ${r * 0.3} ${-r * 0.6} 0 0
      C ${-r * 0.3} ${r * 0.6} ${-r} ${r * 0.6} ${-r} 0
      Z
    `.replace(/\s+/g, ' ').trim();
  }

  /**
   * Generate medical cross icon
   * Educational: Shows geometric construction principles
   */
  private static generateMedicalIcon(radius: number): string {
    const r = radius * 0.7;
    const thickness = r * 0.3;
    // Medical cross using rectangle combination
    return `
      M ${-thickness} ${-r}
      L ${thickness} ${-r}
      L ${thickness} ${-thickness}
      L ${r} ${-thickness}
      L ${r} ${thickness}
      L ${thickness} ${thickness}
      L ${thickness} ${r}
      L ${-thickness} ${r}
      L ${-thickness} ${thickness}
      L ${-r} ${thickness}
      L ${-r} ${-thickness}
      L ${-thickness} ${-thickness}
      Z
    `;
  }

  /**
   * Generate water drop icon
   * Educational: Demonstrates organic shape creation
   */
  private static generateWaterIcon(radius: number): string {
    const r = radius * 0.8;
    // Water drop shape using curves
    return `
      M 0 ${-r}
      C ${-r * 0.6} ${-r * 0.6} ${-r * 0.8} ${r * 0.2} 0 ${r * 0.8}
      C ${r * 0.8} ${r * 0.2} ${r * 0.6} ${-r * 0.6} 0 ${-r}
      Z
    `.replace(/\s+/g, ' ').trim();
  }

  /**
   * Generate IoT connected devices icon
   * Educational: Shows how to create network-like shapes
   */
  private static generateIoTIcon(radius: number): string {
    const r = radius * 0.6;
    // Connected nodes pattern
    return `
      M 0 ${-r}
      L ${r * 0.866} ${r * 0.5}
      L ${-r * 0.866} ${r * 0.5}
      Z
      M 0 ${-r * 0.3}
      L ${r * 0.3} ${r * 0.15}
      L ${-r * 0.3} ${r * 0.15}
      Z
    `;
  }

  /**
   * Generate default graduation cap icon
   * Educational: Academic symbol construction
   */
  private static generateDefaultAcademicIcon(radius: number): string {
    const r = radius * 0.7;
    // Graduation cap silhouette
    return `
      M ${-r} ${-r * 0.2}
      L ${r} ${-r * 0.2}
      L ${r * 0.8} ${r * 0.4}
      L ${-r * 0.8} ${r * 0.4}
      Z
      M ${r * 0.9} ${-r * 0.2}
      L ${r * 1.2} ${-r * 0.8}
      L ${r * 1.1} ${-r * 0.8}
      L ${r * 0.8} ${-r * 0.3}
    `;
  }
}

/**
 * Advanced Shape Morphing Engine
 * Implements smooth interpolation between different shapes
 */
export class ShapeMorphingEngine {
  
  /**
   * Create smooth interpolation between two SVG paths
   * Educational: Demonstrates path interpolation mathematics
   */
  static createPathInterpolator(pathA: string, pathB: string, samples: number = 100): (t: number) => string {
    // Parse both paths and create interpolator
    const interpolator = d3.interpolateString(pathA, pathB);
    
    return (t: number) => {
      // Apply easing function for natural movement
      const easedT = d3.easeBackOut(Math.max(0, Math.min(1, t)));
      return interpolator(easedT);
    };
  }

  /**
   * Create staggered morphing animation for multiple elements
   * Educational: Shows advanced animation choreography
   */
  static createStaggeredMorph(
    elements: d3.Selection<any, any, any, any>,
    fromShape: ShapeType,
    toShape: ShapeType,
    config: MorphConfig
  ): void {
    
    elements.each(function(d: any, i: number) {
      const element = d3.select(this);
      const delay = i * config.stagger;
      
      // Get current and target shapes
      const currentPath = element.attr('d');
      const targetPath = ShapeUtils.generateShapePath(toShape, d.radius || 20);
      
      // Create interpolator
      const interpolator = ShapeMorphingEngine.createPathInterpolator(
        currentPath, 
        targetPath, 
        config.interpolationSamples
      );
      
      // Execute transition with stagger
      element
        .transition()
        .delay(delay)
        .duration(config.duration)
        .ease(config.easing)
        .attrTween('d', () => interpolator);
    });
  }

  /**
   * Create pulsing morph effect for highlighting
   * Educational: Demonstrates rhythm and emphasis in animation
   */
  static createPulseMorph(
    element: d3.Selection<any, any, any, any>,
    baseShape: ShapeType,
    radius: number,
    pulseIntensity: number = 1.5
  ): void {
    
    const basePath = ShapeUtils.generateShapePath(baseShape, radius);
    const pulsePath = ShapeUtils.generateShapePath(baseShape, radius * pulseIntensity);
    
    const interpolator = ShapeMorphingEngine.createPathInterpolator(basePath, pulsePath);
    
    // Create infinite pulsing animation
    element
      .transition()
      .duration(1000)
      .ease(d3.easeSinInOut)
      .attrTween('d', () => (t: number) => interpolator(Math.sin(t * Math.PI)))
      .on('end', () => {
        // Repeat the pulse
        ShapeMorphingEngine.createPulseMorph(element, baseShape, radius, pulseIntensity);
      });
  }
}

/**
 * Utility functions for shape generation routing
 */
export const ShapeUtils = {
  
  /**
   * Generate SVG path for any shape type
   * Educational: Central dispatch pattern for shape generation
   */
  generateShapePath(type: ShapeType, radius: number, config?: Partial<ShapeConfig>): string {
    const defaultConfig: ShapeConfig = {
      radius,
      strokeWidth: 2,
      fillOpacity: 0.8,
      points: 5,
      corners: 6,
      type
    };
    
    const finalConfig = { ...defaultConfig, ...config };
    
    switch (type) {
      case 'circle':
        return AdvancedShapeGenerator.generateCirclePath(finalConfig.radius);
      
      case 'square':
        return AdvancedShapeGenerator.generateSquarePath(finalConfig.radius * 1.4, 2);
      
      case 'star':
        return AdvancedShapeGenerator.generateStarPath(
          finalConfig.radius, 
          finalConfig.points
        );
      
      case 'hexagon':
        return AdvancedShapeGenerator.generatePolygonPath(finalConfig.radius, 6);
      
      case 'triangle':
        return AdvancedShapeGenerator.generatePolygonPath(finalConfig.radius, 3);
      
      case 'diamond':
        return AdvancedShapeGenerator.generatePolygonPath(finalConfig.radius, 4);
      
      case 'academic':
        return AdvancedShapeGenerator.generateAcademicIcon('default', finalConfig.radius);
      
      default:
        return AdvancedShapeGenerator.generateCirclePath(finalConfig.radius);
    }
  },

  /**
   * Get shape-specific academic icon
   * Educational: Domain-specific shape selection
   */
  getAcademicShapePath(domain: string, radius: number): string {
    return AdvancedShapeGenerator.generateAcademicIcon(domain, radius);
  },

  /**
   * Create smooth transition between shapes
   * Educational: Wrapper for easy shape morphing
   */
  morphShape(
    element: d3.Selection<any, any, any, any>,
    fromType: ShapeType,
    toType: ShapeType,
    radius: number,
    duration: number = 800
  ): void {
    const fromPath = this.generateShapePath(fromType, radius);
    const toPath = this.generateShapePath(toType, radius);
    
    const interpolator = ShapeMorphingEngine.createPathInterpolator(fromPath, toPath);
    
    element
      .transition()
      .duration(duration)
      .ease(d3.easeBackOut.overshoot(1.7))
      .attrTween('d', () => interpolator);
  }
};

// Export enhanced utility with educational wrapper
export const advancedShapeUtils = ShapeUtils;

/**
 * EDUCATIONAL REFERENCES & FURTHER READING:
 * 
 * Observable Notebooks:
 * - "Path Interpolation" by Mike Bostock
 * - "Custom SVG Symbols" by Philippe Rivière  
 * - "Shape Morphing Techniques" by D3.js Community
 * 
 * Academic Papers:
 * - "Animated Transitions in Statistical Data Graphics" (Heer & Robertson)
 * - "The Grammar of Graphics" (Wilkinson)
 * 
 * Mathematical Foundations:
 * - Polar Coordinate Systems and Trigonometry
 * - Bézier Curve Mathematics and Interpolation
 * - Computational Geometry Principles
 * - SVG Path Data Format Specification
 * 
 * Community Resources:
 * - D3.js Discord: Advanced Techniques Channel
 * - Reddit r/dataisbeautiful: D3.js Shape Morphing Posts
 * - YouTube: "Advanced D3.js Animations" Tutorial Series
 */
