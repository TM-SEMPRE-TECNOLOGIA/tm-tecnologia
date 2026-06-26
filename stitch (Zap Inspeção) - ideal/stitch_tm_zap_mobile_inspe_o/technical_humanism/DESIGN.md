---
name: Technical Humanism
colors:
  surface: '#faf9f6'
  surface-dim: '#dbdad7'
  surface-bright: '#faf9f6'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f4f3f0'
  surface-container: '#efeeeb'
  surface-container-high: '#e9e8e5'
  surface-container-highest: '#e3e2df'
  on-surface: '#1b1c1a'
  on-surface-variant: '#584239'
  inverse-surface: '#2f312f'
  inverse-on-surface: '#f2f1ee'
  outline: '#8b7168'
  outline-variant: '#dfc0b5'
  surface-tint: '#a53c00'
  primary: '#a13a00'
  on-primary: '#ffffff'
  primary-container: '#c45119'
  on-primary-container: '#fffbff'
  inverse-primary: '#ffb598'
  secondary: '#605e59'
  on-secondary: '#ffffff'
  secondary-container: '#e6e2db'
  on-secondary-container: '#66645f'
  tertiary: '#3c6629'
  on-tertiary: '#ffffff'
  tertiary-container: '#54803f'
  on-tertiary-container: '#f8ffee'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#ffdbce'
  primary-fixed-dim: '#ffb598'
  on-primary-fixed: '#370e00'
  on-primary-fixed-variant: '#7e2c00'
  secondary-fixed: '#e6e2db'
  secondary-fixed-dim: '#cac6c0'
  on-secondary-fixed: '#1c1c18'
  on-secondary-fixed-variant: '#484742'
  tertiary-fixed: '#bff0a3'
  tertiary-fixed-dim: '#a4d489'
  on-tertiary-fixed: '#062100'
  on-tertiary-fixed-variant: '#285015'
  background: '#faf9f6'
  on-background: '#1b1c1a'
  surface-variant: '#e3e2df'
  ink-primary: '#1A1A1A'
  ink-subtle: '#8C8A85'
  border-base: '#DAD7D0'
  bubble-sent: '#FBEDE3'
  surface-card: '#FFFFFF'
typography:
  headline-lg:
    fontFamily: Roboto Slab
    fontSize: 28px
    fontWeight: '700'
    lineHeight: 36px
    letterSpacing: -0.01em
  headline-md:
    fontFamily: Roboto Slab
    fontSize: 22px
    fontWeight: '600'
    lineHeight: 28px
  headline-sm:
    fontFamily: Roboto Slab
    fontSize: 18px
    fontWeight: '600'
    lineHeight: 24px
  body-lg:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  body-md:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
  body-sm:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '400'
    lineHeight: 16px
  label-mono:
    fontFamily: JetBrains Mono
    fontSize: 12px
    fontWeight: '500'
    lineHeight: 12px
    letterSpacing: 0.05em
  button:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '600'
    lineHeight: 20px
    letterSpacing: 0.01em
rounded:
  sm: 0.125rem
  DEFAULT: 0.25rem
  md: 0.375rem
  lg: 0.5rem
  xl: 0.75rem
  full: 9999px
spacing:
  baseline: 4px
  container-margin: 16px
  gutter: 12px
  card-padding: 16px
  stack-gap: 8px
---

## Brand & Style
The design system balances technical precision with a warm, human-centric touch. It is designed for construction professionals who require the reliability of a tool like Linear and the approachable communication flow of WhatsApp. 

The aesthetic is **Modern-Tactile**: it avoids the coldness of high-tech SaaS by utilizing a "Cream Paper" base, evoking the feel of physical architectural plans and site journals. It prioritizes information density and clear hierarchy to ensure efficiency during high-stakes site inspections. The style is flat and structural, using purposeful borders and rhythmic spacing rather than heavy gradients or decorative effects.

## Colors
The palette is grounded in earth tones to reflect the construction environment. 
- **Primary (Brick Orange):** Used for critical actions, branding, and status indicators.
- **Backgrounds:** The interface avoids pure white (#FFFFFF) for global backgrounds, opting for a "Cream Paper" (#F5F4F1) to reduce eye strain and provide a premium, tactile feel.
- **Functional Greens:** Success states and completed inspections use a "Forest Green" (#4F7A3A) which maintains a professional, non-neon tone.
- **Messaging:** We utilize a two-tone system for information delivery—Neutral White for received information/cards and Light Orange (#FBEDE3) for sent actions or highlights.

## Typography
The typography system uses a tri-font approach to categorize information types:
- **Serif (Roboto Slab):** Used exclusively for headers and brand-level titles to inject authority and warmth.
- **Sans-Serif (Inter):** The workhorse for all UI elements, inputs, and body text. It is optimized for legibility at high densities.
- **Monospace (JetBrains Mono):** Reserved for technical metadata, ID codes, timestamps, and technical badges. It signals "raw data" vs "human narrative."

## Layout & Spacing
This design system utilizes a **Fixed-Fluid Hybrid** model. While the layout is responsive to the PWA viewport, content resides within a max-width container on larger screens to maintain the focused density characteristic of professional tools.

- **Grid:** 8px base grid system for all layout components.
- **Density:** Elements are tightly packed (Linear-inspired) to minimize scrolling during inspections, using 12px gutters between cards.
- **Reflow:** On mobile, margins reduce to 16px. On desktop, sidebars remain fixed at 280px to facilitate a "Command Center" feel.

## Elevation & Depth
Depth is conveyed through **Tonal Stacking** and **Subtle Structural Shadows**.
- **Level 0 (Background):** Cream Paper (#F5F4F1).
- **Level 1 (Cards/Bubbles):** Pure White (#FFFFFF) with a 1px border (#DAD7D0) and a very soft, low-blur shadow (y: 2px, b: 4px, opacity: 0.05).
- **Level 2 (Modals/Bottom Sheets):** Pure White with a 10% opacity shadow and a 2px top-accent border.
- **Signifiers:** Use a 3px solid vertical accent (Primary Orange) on the left edge of cards to denote "Active" or "Important" status, rather than using heavy shadows.

## Shapes
The shape language is "Soft-Technical." Elements use a **4px corner radius (Soft)** for buttons and cards to feel professional and sturdy. 
- **Bottom Sheets:** Feature a more pronounced 16px top-only radius to create a distinct tactile "pull-up" interaction.
- **Chat Bubbles:** Follow the 4px standard but utilize a "tail" or directional corner to mimic familiar messaging patterns.
- **Avoid:** Do not use fully rounded pill-shaped buttons; maintain the rectangular structural integrity.

## Components
- **Buttons:** Primary buttons use the Brick Orange background with White text. Secondary buttons use the Cream Paper background with a Border-base outline and Primary Ink text. 
- **Cards:** White background with a 1px border and a 3px left-side accent in Brick Orange. Padding is fixed at 16px.
- **Chat Bubbles:** Received bubbles are White with Border-base outlines. Sent bubbles use the Light Orange (#FBEDE3) background.
- **Badges:** Small, rectangular containers with 2px radius. They use JetBrains Mono text in uppercase for a technical, "tagged" appearance.
- **Input Fields:** Flat White background, 1px border. On focus, the border thickens to 2px in Brick Orange. Labels use Inter (600 weight).
- **Headers:** Fixed top navigation with a clear white background or a subtle blur. Titles must be Roboto Slab in Brick Orange.
- **Bottom Sheets:** Large 16px top-rounded containers used for detailed inspection forms or photo uploads.