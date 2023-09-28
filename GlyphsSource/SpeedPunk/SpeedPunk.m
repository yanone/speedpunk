//
//  SpeedPunk.m
//  SpeedPunk
//
//  Created by Georg Seifert on 27.09.23.
//
//

#import "SpeedPunk.h"
#import <GlyphsCore/GlyphsFilterProtocol.h>
#import <GlyphsCore/GSFilterPlugin.h>
#import <GlyphsCore/GSFont.h>
#import <GlyphsCore/GSGlyph.h>
#import <GlyphsCore/GSLayer.h>
#import <GlyphsCore/GSPath.h>
#import <GlyphsCore/GSPathSegment.h>
#import <GlyphsCore/GSGeometrieHelper.h>
#import <GlyphsCore/GSProxyShapes.h>
#import <GlyphsCore/GSSaveBezierPath.h>
#import <GlyphsCore/GSWindowControllerProtocol.h>

extern void calcQuadraticParameters(NSPoint p1, NSPoint p2, NSPoint p3, NSPoint *a, NSPoint *b, NSPoint *c);
extern void calcCubicParameters(NSPoint p1, NSPoint p2, NSPoint p3, NSPoint p4, NSPoint *a, NSPoint *b, NSPoint *c, NSPoint *d);

// int TOTALSEGMENTS = min(int(Stamina() * .00000008), 1000)
int TOTALSEGMENTS = 250;

int MINSEGMENTS = 5;

CGFloat curveGainMin = .1;
CGFloat curveGainMax = 3;

int outsideOfGlyph = 0; // index of selected radio button
int outsideOfCurve = 1;

static NSString *IllustrationPositionIndexKey = @"de.yanone.speedPunk.illustrationPositionIndex";
static NSString *CurveGainKey = @"de.yanone.speedPunk.curveGain";
static NSString *AlphaKey = @"de.yanone.speedPunk.alpha";

CGFloat CurveGain;
int IllustrationPosition;
CGFloat Alpha;

#define drawfactor .01

#if 0 // HSB
static CGFloat Colors[3][3] = {
	{0.588235, 0.108974, 0.611765},
	{0.101928, 1.000000, 0.949020},
	{0.941997, 1.000000, 0.890196},
};
#else
static CGFloat Colors[3][3] = {
	{(0x8b / 255.0), (0x93 / 255.0), (0x9c / 255.0)},
	{(0xf2 / 255.0), (0x94 / 255.0), (0x00 / 255.0)},
	{(0xe3 / 255.0), (0x00 / 255.0), (0x4f / 255.0)},
};
#endif


CGFloat solveCubicBezierCurvature(NSPoint a, NSPoint b, NSPoint c, NSPoint d, NSPoint *r1, NSPoint *r2, NSPoint *r3, CGFloat t) {
	/*
	 Calc curvature using cubic Bezier equation and 1st and 2nd derivative.
	 Returns position of on-curve point p1234, and vector of 1st and 2nd derivative.
	 */

	CGFloat t3 = t * t * t;
	CGFloat t2 = t * t;
	r1->x = a.x * t3 + b.x * t2 + c.x * t + d.x;
	r1->y = a.y * t3 + b.y * t2 + c.y * t + d.y;


	r2->x = 3 * a.x * t2 + 2 * b.x * t + c.x;
	r2->y = 3 * a.y * t2 + 2 * b.y * t + c.y;


	r3->x = 6 * a.x * t + 2 * b.x;
	r3->y = 6 * a.y * t + 2 * b.y;

	return (r2->x * r3->y - r2->y * r3->x) / pow(r2->x * r2->x + r2->y * r2->y, 1.5);
}

CGFloat solveQuadraticBezierCurvature(NSPoint a, NSPoint b, NSPoint c, NSPoint *r1, NSPoint *r2, NSPoint *r3, CGFloat t) {
	/*
	 Calc curvature using quadratic Bezier equation and 1st and 2nd derivative.
	 Returns position of on-curve point p123, and vector of 1st and 2nd derivative.
	 */
	CGFloat t2 = t * t;
	r1->x = a.x * t2 + b.x * t + c.x;
	r1->y = a.y * t2 + b.y * t + c.y;


	r2->x = 2 * a.x * t + b.x;
	r2->y = 2 * a.y * t + b.y;


	r3->x = 2 * a.x;
	r3->y = 2 * a.y;

	//return (r, r1, r2, (r1.x * r2.y - r1.y * r2.x) / (r1.x ** 2 + r1.y ** 2) ** 1.5)
	return (r2->x * r3->y - r2->y * r3->x) / pow(r2->x * r2->x + r2->y * r2->y, 1.5);
}

CGFloat Interpolate(CGFloat a, CGFloat b, CGFloat p) {
	/*
	 Interpolate between values a and b at float position p (0-1)
	 Limit: No extrapolation
	*/
	CGFloat i = a + (b - a) * p;
	return i;
}

void InterpolateHexColorList(CGFloat colors[3][3], CGFloat p, CGFloat *R, CGFloat *G, CGFloat *B) {
	/*
	 Interpolate between list of hex RRGGBB values at float position p (0-1)
	 Returns float list (R, G, B)
	*/

	if (p <= 0) {
		CGFloat *color = colors[0];
		*R = color[0];
		*G = color[1];
		*B = color[2];
		return;
	}
	else if (p >= 1) {
		CGFloat *color = colors[2];
		*R = color[0];
		*G = color[1];
		*B = color[2];
		return;
	}
	else {
		int count = 3; //(int)colors;

		for (int i = 0; i < count; i++) {

			CGFloat before = i / (CGFloat)(count - 1);
			CGFloat after = (i + 1) / (CGFloat)(count - 1);

			if (before < p && p < after) {
				CGFloat v = (p - before) / (after - before);

				// print("interpolate between", before, after, p, v)
				CGFloat *color1 = colors[i];
				CGFloat *color2 = colors[i + 1];
				*R = Interpolate(color1[0], color2[0], v);
				*G = Interpolate(color1[1], color2[1], v);
				*B = Interpolate(color1[2], color2[2], v);
			}
			else if (p == before) {
				CGFloat *color = colors[i];
				*R = color[0];
				*G = color[1];
				*B = color[2];
				return;
			}
			else if (p == after) {
				CGFloat *color = colors[i + 1];
				*R = color[0];
				*G = color[1];
				*B = color[2];
				return;
			}
		}
	}
}

@interface SPCurvature : NSObject

- (instancetype)initWithCurvature1:(CGFloat)curvature1 r1:(NSPoint)r1 r2:(NSPoint)r2 q1:(NSPoint)q1 q2:(NSPoint)q2 curvature2:(CGFloat)curvature2;

- (void)draw;

@property (nonatomic, weak) SPSpeedPunk *speedPunk;
@property (nonatomic) float curvature1;
@property (nonatomic) float curvature2;
@property (nonatomic) NSPoint r1;
@property (nonatomic) NSPoint r2;
@property (nonatomic) NSPoint q1;
@property (nonatomic) NSPoint q2;

@property (nonatomic) float vmin;
@property (nonatomic) float vmax;

@property (nonatomic, strong) NSBezierPath *path;
@property (nonatomic, strong) NSColor *color;

@end

@interface SPSpeedPunk ()

@property (nonatomic, strong) NSMutableArray <SPCurvature *> *segments;
@property (nonatomic, weak) GSLayer *lastLayer;
@property (nonatomic) NSTimeInterval lastUpdate;
@property (nonatomic) CGFloat unitsperem;

@end

@implementation SPCurvature

- (instancetype)initWithCurvature1:(CGFloat)curvature1 r1:(NSPoint)r1 r2:(NSPoint)r2 q1:(NSPoint)q1 q2:(NSPoint)q2 curvature2:(CGFloat)curvature2 {
	self = [self init];
	_curvature1 = curvature1;
	_curvature2 = curvature2;
	_r1 = r1;
	_r2 = r2;
	_q1 = q1;
	_q2 = q2;
	return self;
}

- (void)draw {
	// update color
	if (!self.color) {
		if (![self updateColor]) {
			return; // can happen with straight segments
		}
	}
	if (!self.path) {
		[self updateCurvaturePath];
	}
	[self drawCurvaturePaths];
}

- (CGFloat)Value {
	return (fabs(self.curvature1 * drawfactor) + fabs(self.curvature2 * drawfactor)) / 2.0;
}

- (BOOL)updateColor {
	// Color
	CGFloat deltaV = _vmax - _vmin;

	if (fabs(deltaV) < 0.0000001) {
		return NO;
	}
	CGFloat p = ([self Value] - _vmin) / deltaV;
	CGFloat R = 1, G = 0, B = 0;
	//InterpolateHexColorList(colors[_speedPunk.curves], p);
	InterpolateHexColorList(Colors, p, &R, &G, &B);

	self.color = [NSColor colorWithCalibratedRed:R green:G blue:B alpha:Alpha];
	//self.color = [NSColor colorWithCalibratedHue:R saturation:G brightness:B alpha:A];
	return YES;
}

- (void)updateCurvaturePath {
	// Recalc illustration
	CGFloat factor = drawfactor * CurveGain * pow(_speedPunk.unitsperem, 2);
	CGFloat k1 = self.curvature1 * factor;
	CGFloat k2 = self.curvature2 * factor;

	if (IllustrationPosition == outsideOfGlyph) {
		k1 = fabs(k1);
		k2 = fabs(k2);
#if 0
		// TrueType
		if (speedpunklib.curves == 'quadratic') {
			k1 = -k1;
			k2 = -k2;
		}
#endif
	}
	// Define points
	NSPoint S10 = self.r1;
	NSPoint S11 = self.r2;
	NSPoint S20 = self.q1;
	NSPoint S21 = self.q2;
	//self.oncurve1 = S10
	//self.oncurve2 = S20
	CGFloat S21abs = sqrt(S21.x * S21.x + S21.y * S21.y);
	CGFloat S11abs = sqrt(S11.x * S11.x + S11.y * S11.y);
	NSPoint outerspace2 = NSMakePoint(S20.x + (S21.y / S21abs * k2), S20.y - (S21.x / S21abs * k2));
	NSPoint outerspace1 = NSMakePoint(S10.x + (S11.y / S11abs * k1), S10.y - (S11.x / S11abs * k1));

	NSBezierPath *path = [GSSaveBezierPath new];
	// OnCurve
	[path moveToPoint:S10];
	[path lineToPoint:S20];
	// Outer points
	[path lineToPoint:outerspace2];
	[path lineToPoint:outerspace1];
	[path closePath];
	self.path = path;
}

- (void)drawCurvaturePaths {
	if (!self.color) {
		return;
	}
	[self.color setFill];
	[self.path fill];
}

@end

@implementation SPSpeedPunk

@synthesize controller = _editViewController;

+ (void)initialize {
	NSUserDefaults *defaults = NSUserDefaults.standardUserDefaults;
	CGFloat defaultCurveGain = Interpolate(curveGainMin, curveGainMax, .2);
	[defaults registerDefaults:@{
		CurveGainKey: @(defaultCurveGain),
		AlphaKey: @0.7
	}];
	CurveGain = [defaults floatForKey:CurveGainKey];
	IllustrationPosition = (int)[defaults integerForKey:IllustrationPositionIndexKey];
	Alpha = [defaults floatForKey:AlphaKey];
}

- (instancetype)init {
	self = [super initWithNibName:@"settingsView" bundle:[NSBundle bundleForClass:[self class]]];
	[self view];
	return self;
}

- (void)awakeFromNib {
	NSBundle *bundle = [NSBundle bundleForClass:[self class]];
	NSString *versionString = bundle.infoDictionary[@"CFBundleShortVersionString"];
	NSString *string = NSLocalizedStringFromTableInBundle(@"Speed Punk v%@ Settings", nil, bundle, @"Plugin Title");
	string = [NSString stringWithFormat:string, versionString];
	self.titleField.stringValue = string;

	self.gainSlider.minValue = curveGainMin;
	self.gainSlider.maxValue = curveGainMax;

	NSUserDefaultsController *defaultsController = NSUserDefaultsController.sharedUserDefaultsController;
	[defaultsController addObserver:self forKeyPath:[@"values." stringByAppendingString:IllustrationPositionIndexKey] options:0 context:(__bridge void *)(IllustrationPositionIndexKey)];
	[defaultsController addObserver:self forKeyPath:[@"values." stringByAppendingString:CurveGainKey] options:0 context:(__bridge void *)(CurveGainKey)];
	[defaultsController addObserver:self forKeyPath:[@"values." stringByAppendingString:AlphaKey] options:0 context:(__bridge void *)(AlphaKey)];
}

- (NSUInteger)interfaceVersion {
	// Distinguishes the API verison the plugin was built for. Return 1.
	return 1;
}

- (NSString *)title {
	// This is the name as it appears in the menu in combination with 'Show'.
	// E.g. 'return @"Nodes";' will make the menu item read "Show Nodes".
	return @"Speed Punk";
}

- (NSString *)keyEquivalent {
	// The key for the keyboard shortcut. Set modifier keys in modifierMask further below.
	// Pretty tricky to find a shortcut that is not taken yet, so be careful.
	// If you are not sure, use 'return nil;'. Users can set their own shortcuts in System Prefs.
	return @"x";
}

- (NSEventModifierFlags)modifierMask {
	// Use any combination of these to determine the modifier keys for your default shortcut:
	// return NSShiftKeyMask | NSControlKeyMask | NSCommandKeyMask | NSAlternateKeyMask;
	// Or:
	// return 0;
	// ... if you do not want to set a shortcut.
	return 0;
}

- (void)observeValueForKeyPath:(NSString *)keyPath ofObject:(id)object change:(NSDictionary<NSKeyValueChangeKey,id> *)change context:(void *)context {
	if ((__bridge NSString *)context == IllustrationPositionIndexKey ||
		(__bridge NSString *)context == CurveGainKey) {
		NSUserDefaults *defaults = NSUserDefaults.standardUserDefaults;
		CurveGain = [defaults floatForKey:CurveGainKey];
		IllustrationPosition = (int)[defaults integerForKey:IllustrationPositionIndexKey];

		self.segments = nil;
		[self.controller redraw];
		return;
	}
	if ((__bridge NSString *)context == AlphaKey) {
		NSUserDefaults *defaults = NSUserDefaults.standardUserDefaults;
		Alpha = [defaults floatForKey:AlphaKey];

		for (GSPathSegment *segment in self.segments) {
			for (SPCurvature *curvatrue in segment.objects) {
				curvatrue.color = nil;
			}
		}
		[self.controller redraw];
		return;
	}
}

- (void)addMenuItemsForEvent:(nonnull NSEvent *)theEvent toMenu:(nonnull NSMenu *)theMenu {
	NSMenuItem *menuItem = [[NSMenuItem alloc] initWithTitle:@"Speed Punk" action:nil keyEquivalent:@""];
	menuItem.view = self.view;
	[theMenu addItem:NSMenuItem.separatorItem];
	[theMenu addItem:menuItem];
	[theMenu addItem:NSMenuItem.separatorItem];
}

- (NSArray *)_calcCurvaturesCubic:(NSPoint)p1 p2:(NSPoint)p2 p3:(NSPoint)p3 p4:(NSPoint)p4 steps:(int)steps {

	NSMutableArray *curvatureSets = [NSMutableArray new];
	NSPoint a, b, c, d;
	calcCubicParameters(p1, p2, p3, p4, &a, &b, &c, &d);

	CGFloat curvature1 = NSNotFound;
	CGFloat curvature2 = NSNotFound;
	NSPoint q1 = NSZeroPoint;
	NSPoint q2 = NSZeroPoint;
	for (int idx = 0; idx <= steps; idx++) {
		CGFloat t = idx / (CGFloat)steps;
		NSPoint r1, r2, r3;
		curvature1 = solveCubicBezierCurvature(a, b, c, d, &r1, &r2, &r3, t);
		if (curvature2 < NSNotFound) {
			SPCurvature *curve = [[SPCurvature alloc] initWithCurvature1:curvature1 r1:r1 r2:r2 q1:q1 q2:q2 curvature2:curvature2];
			curve.speedPunk = self;
			[curvatureSets addObject:curve];
		}
		q1 = r1;
		q2 = r2;
		curvature2 = curvature1;
	}
	return curvatureSets;
}

- (NSArray *)_calcCurvaturesQuadratic:(NSPoint)p1 p2:(NSPoint)p2 p3:(NSPoint)p3 steps:(int)steps {

	NSMutableArray *curvatureSets = [NSMutableArray new];
	NSPoint a, b, c;
	calcQuadraticParameters(p1, p2, p3, &a, &b, &c);

	CGFloat curvature1 = NSNotFound;
	CGFloat curvature2 = NSNotFound;
	NSPoint q1 = NSZeroPoint;
	NSPoint q2 = NSZeroPoint;
	for (int idx = 0; idx <= steps; idx++) {
		CGFloat t = idx / (CGFloat)steps;
		NSPoint r1, r2, r3;
		curvature1 = solveQuadraticBezierCurvature(a, b, c, &r1, &r2, &r3, t);
		if (curvature2 < NSNotFound) {
			SPCurvature *curve = [[SPCurvature alloc] initWithCurvature1:curvature1 r1:r1 r2:r2 q1:q1 q2:q2 curvature2:curvature2];
			curve.speedPunk = self;
			[curvatureSets addObject:curve];
		}
		q1 = r1;
		q2 = r2;
		curvature2 = curvature1;
	}
	return curvatureSets;
}

- (void)calcCurvatures:(GSPathSegment *)segment steps:(int)steps {
	NSArray *curvatureSets;
	if( segment.type == CURVE) {
		// curvatureSets = self._calcCurvaturesCubic(segment[0], segment[1], segment[2], segment[3], steps)
		curvatureSets = [self _calcCurvaturesCubic:segment->elements[0] p2:segment->elements[1] p3:segment->elements[2] p4:segment->elements[3] steps:steps];
	}
	else if (segment.type == QCURVE) {
		if (segment->count == 3) {
			curvatureSets = [self _calcCurvaturesQuadratic:segment->elements[0] p2:segment->elements[1] p3:segment->elements[2] steps:steps];
		}
		else {
			curvatureSets = [NSMutableArray new];
			NSPoint prevOn = segment->elements[0];
			int idx = 1;
			for (; idx < segment->count - 2; idx++) {
				NSPoint nextOn = GSScalePoint(GSAddPoints(segment->elements[idx], segment->elements[idx + 1]), 0.5);
				NSArray *segmentCurvatureSets = [self _calcCurvaturesQuadratic:prevOn p2:segment->elements[idx] p3:nextOn steps:steps];
				prevOn = nextOn;
				[(NSMutableArray *)curvatureSets addObjectsFromArray:segmentCurvatureSets];
			}
			NSArray *segmentCurvatureSets = [self _calcCurvaturesQuadratic:prevOn p2:segment->elements[idx] p3:segment->elements[idx + 1] steps:steps];
			[(NSMutableArray *)curvatureSets addObjectsFromArray:segmentCurvatureSets];
		}
	}
	[segment setObjects:curvatureSets];
}

- (void)gatherSegments:(GSLayer *)layer {

	self.unitsperem = layer.font.unitsPerEm;

	NSMutableArray *newSegments = [NSMutableArray new];
	for (GSPath *path in layer.paths) {
		for (GSPathSegment *segment in [path segments]) {
			if (segment.type == CURVE || segment.type == QCURVE) {
				[newSegments addObject:segment];
			}
		}
	}
	self.segments = newSegments;
	if (newSegments.count == 0) {
		return;
	}
	int steps = (int)MAX(TOTALSEGMENTS / newSegments.count, MINSEGMENTS - 1);
	CGFloat vmin = 1000;
	CGFloat vmax = -1000;
	for (GSPathSegment *segment in newSegments) {
		[self calcCurvatures:segment steps:steps];
		for (SPCurvature *curvature in segment.objects) {
			CGFloat value = [curvature Value];
			vmin = MIN(vmin, value);
			vmax = MAX(vmax, value);
		}
	}

	for (GSPathSegment *segment in newSegments) {
		[self calcCurvatures:segment steps:steps];
		for (SPCurvature *curvature in segment.objects) {
			curvature.vmin = vmin;
			curvature.vmax = vmax;
		}
	}
}

- (void)updatePunk:(GSLayer *)layer {
	if (layer != _lastLayer) {
		_segments = nil;
	}
	if (_lastUpdate < layer.lastUpdate) {
		_segments = nil;
	}
	if (!_segments) {
		[self gatherSegments:layer];
		_lastUpdate = layer.lastUpdate;
		_lastLayer = layer;
	}
}

- (BOOL)conditionsAreMetForDrawing {
	/*
	 Don't activate if text or pan (hand) tool are active.
	 */
	NSWindowController <GSWindowControllerProtocol> *currentController = self.controller.view.window.windowController;
	if (!currentController) {
		return NO;
	}
	id tool = [currentController toolDrawDelegate];
	BOOL textToolIsActive = [tool isKindOfClass:NSClassFromString(@"GlyphsToolText")];
	BOOL handToolIsActive = [tool isKindOfClass:NSClassFromString(@"GlyphsToolHand")];
	if (!textToolIsActive && !handToolIsActive) {
		return YES;
	}
	return NO;
}

- (void)drawBackgroundForLayer:(GSLayer*)layer options:(NSDictionary *)options {
	// Whatever you draw here will be displayed BEHIND the paths.
	if (!self.conditionsAreMetForDrawing) {
		return;
	}
	[self updatePunk:layer];
	for (GSPathSegment *segment in self.segments) {
		for (SPCurvature *curvature in segment.objects) {
			[curvature draw];
		}
	}
}

- (IBAction)visitWebsite:(id)sender {
	[NSWorkspace.sharedWorkspace openURL:[NSURL URLWithString:@"https://github.com/yanone/speedpunk"]];
};

- (IBAction)visitTwitter:(id)sender {
	[NSWorkspace.sharedWorkspace openURL:[NSURL URLWithString:@"https://twitter.com/yanone"]];
};

@end
