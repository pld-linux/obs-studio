# TODO:
# - AJA (BR: libajantv2)
# - system librnnoise
# - disabled modules: aja aja-output-ui obs-libfdk obs-webrtc
#
# Conditional build:
%bcond_with	aja	# AJA NTV2 support
%bcond_without	jack	# JACK support
%bcond_with	qt5	# Qt 5 instead of Qt 6
%bcond_with	webrtc	# Build WebRTC output plugin (R: LibDataChannel)

%ifnarch %{x8664}
# plugins/aja/cmake/legacy.cmake: "aja support not enabled (32-bit not supported)."
%undefine	with_aja
%endif
Summary:	OBS Studio - live streaming and screen recording software
Summary(pl.UTF-8):	OBS Studio - oprogramowanie do przesyłania strumieni na żywo i nagrywania ekranu
Name:		obs-studio
Version:	32.1.2
Release:	1
License:	GPL v2+
Group:		X11/Applications/Multimedia
#Source0Download: https://github.com/obsproject/obs-studio/releases
Source0:	https://github.com/obsproject/obs-studio/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	48714ec4e527e9044c6653e1996d8884
Patch0:		disable-missing-plugins.patch
Patch1:		size_t.patch
Patch2:		x32.patch
Patch3:		sign-compare.patch
Patch4:		x11-linkage.patch
Patch5:		luajit-lua52.patch
Patch6:		no-arch-abi-warning.patch
Patch7:		format-string.patch
URL:		https://obsproject.com/
BuildRequires:	EGL-devel
BuildRequires:	ImageMagick-devel
BuildRequires:	OpenGL-devel
BuildRequires:	OpenGL-GLX-devel
BuildRequires:	alsa-lib-devel
BuildRequires:	cmake >= 3.16
BuildRequires:	curl-devel
BuildRequires:	dbus-devel
# avcodec avfilter avdevice avutil swscale avformat swresample
BuildRequires:	ffmpeg-devel >= 6.1
BuildRequires:	fontconfig-devel
BuildRequires:	freetype-devel >= 2
BuildRequires:	glib2-devel >= 1:2.76
%{?with_jack:BuildRequires:	jack-audio-connection-kit-devel}
BuildRequires:	jansson-devel >= 2.5
%{?with_aja:BuildRequires:	libajantv2-devel}
BuildRequires:	libdrm-devel
BuildRequires:	librist-devel
BuildRequires:	libstdc++-devel >= 6:4.7
BuildRequires:	libuuid-devel
BuildRequires:	libv4l-devel
BuildRequires:	libva-devel
BuildRequires:	libvpl-devel >= 2.9
BuildRequires:	libx264-devel
BuildRequires:	nlohmann-json-devel
# xcb xcb-composite xcb-randr xcb-shm xcb-xfixes xcb-xinerama
BuildRequires:	libxcb-devel
%ifnarch x32
BuildRequires:	luajit-devel
%endif
BuildRequires:	mbedtls-devel
BuildRequires:	nv-codec-headers >= 12
BuildRequires:	pciutils-devel
BuildRequires:	pipewire-devel >= 0.3.33
BuildRequires:	pkgconfig
BuildRequires:	pulseaudio-devel
BuildRequires:	python3-devel >= 1:3.8
BuildRequires:	rpmbuild(macros) >= 1.605
BuildRequires:	simde-devel
BuildRequires:	speexdsp-devel
BuildRequires:	srt-devel
BuildRequires:	swig-python >= 4
BuildRequires:	udev-devel
BuildRequires:	uthash-devel
BuildRequires:	vlc-devel
# wayland-client
BuildRequires:	wayland-devel
BuildRequires:	wayland-egl-devel
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libxkbcommon-devel
BuildRequires:	zlib-devel
%if %{with qt5}
BuildRequires:	Qt5Core-devel >= 5
BuildRequires:	Qt5Gui-devel >= 5
BuildRequires:	Qt5Network-devel >= 5
BuildRequires:	Qt5Svg-devel >= 5
BuildRequires:	Qt5Widgets-devel >= 5
BuildRequires:	Qt5Xml-devel >= 5
BuildRequires:	qt5-build >= 5
BuildRequires:	qt5-qmake >= 5
%else
BuildRequires:	Qt6Core-devel >= 6
BuildRequires:	Qt6Gui-devel >= 6
BuildRequires:	Qt6Network-devel >= 6
BuildRequires:	Qt6Svg-devel >= 6
BuildRequires:	Qt6Widgets-devel >= 6
BuildRequires:	Qt6Xml-devel >= 6
BuildRequires:	qt6-build >= 6
BuildRequires:	qt6-qmake >= 6
%endif
Requires:	glib2 >= 1:2.76
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_noautoprovfiles	%{_libdir}/obs-plugins

# symbols from libm confuse the checker
%define		skip_post_check_so	libobs.so.*

%description
OBS Studio is software designed for capturing, compositing, encoding,
recording, and streaming video content, efficiently.

%description -l pl.UTF-8
OBS Studio to oprogramowanie służące do wydajnego przechwytywania,
składania, kodowania, nagrywania i przesyłania treści wideo.

%package devel
Summary:	Header files for OBS Studio
Summary(pl.UTF-8):	Pliki nagłówkowe OBS Studio
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for OBS Studio.

%description devel -l pl.UTF-8
Pliki nagłówkowe OBS Studio.

%prep
%setup -q
%patch -P 0 -p1
%patch -P 1 -p1
%patch -P 2 -p1
%patch -P 3 -p1
%patch -P 4 -p1
%patch -P 5 -p1
%patch -P 6 -p1
%patch -P 7 -p1

%build
export OBS_MULTIARCH_SUFFIX="%(echo "%{_lib}" | sed -e 's/^lib//')"
%cmake -B build \
	-DCMAKE_INSTALL_BINDIR:PATH=bin \
	-DCMAKE_INSTALL_INCLUDEDIR:PATH=include \
	-DCMAKE_INSTALL_DATAROOTDIR:PATH=share \
	-DCMAKE_INSTALL_DATADIR:PATH=share \
	-DCMAKE_INSTALL_LIBDIR:PATH=%{_lib} \
	-DCMAKE_SKIP_RPATH=1 \
	-DBUILD_BROWSER=OFF \
	-DCALM_DEPRECATION=ON \
	%{!?with_aja:-DENABLE_AJA=OFF} \
	%{?with_jack:-DENABLE_JACK=ON} \
%ifarch x32
	-DENABLE_SCRIPTING_LUA=OFF \
%endif
	%{!?with_webrtc:-DENABLE_WEBRTC=OFF} \
	-DOBS_VERSION_OVERRIDE=%{version} \
	-DQT_VERSION=%{?with_qt5:5}%{!?with_qt5:6} \
	-DUNIX_STRUCTURE=1

%{__make} -C build

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install/fast \
        DESTDIR=$RPM_BUILD_ROOT

builddir="$(pwd)"

cd $RPM_BUILD_ROOT
reldatadir="$(echo %{_datadir} | sed -e 's,^/,,')"
for f in $reldatadir/obs/obs-studio/locale/??*.ini $reldatadir/obs/obs-plugins/*/locale/??*.ini ; do
	locale="$(basename "$f" .ini | tr - _)"
	case "$locale" in
	  en_US)
		loctag=""
		;;
	  pt_BR|zh_CN|zh_TW)
		loctag="%lang($locale) "
		;;
	  *)
		# this rule covers also conversion of bogus Serbian codes to "sr": "sr_CS" (actually sr_RS@latin), "sr_SP" (actually sr_RS, cyrillic)
		loctag="%lang(${locale%_??}) "
		;;
	esac
	echo "${loctag}/$f"
done > "$builddir/%{name}.lang"

# dir guard
%{__rm} $RPM_BUILD_ROOT%{_datadir}/obs/obs-plugins/{decklink-captions,decklink-output-ui}/.keepme
%{__rm} $RPM_BUILD_ROOT%{_datadir}/obs/obs-plugins/linux-pipewire/.gitkeep

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS README.rst
%attr(755,root,root) %{_bindir}/obs
%attr(755,root,root) %{_bindir}/obs-ffmpeg-mux
%attr(755,root,root) %{_bindir}/obs-nvenc-test
%{_libdir}/libobs-frontend-api.so.30
%ghost %{_libdir}/libobs-frontend-api.so.0
%{_libdir}/libobs-opengl.so.30
%{_libdir}/libobs.so.30
%ghost %{_libdir}/libobs.so.0
%{_libdir}/libobs-scripting.so.30

%dir %{_libdir}/obs-plugins
%{_libdir}/obs-plugins/decklink-captions.so
%{_libdir}/obs-plugins/decklink-output-ui.so
%{_libdir}/obs-plugins/decklink.so
%{_libdir}/obs-plugins/frontend-tools.so
%{_libdir}/obs-plugins/image-source.so
%{_libdir}/obs-plugins/linux-alsa.so
%{_libdir}/obs-plugins/linux-capture.so
%if %{with jack}
%{_libdir}/obs-plugins/linux-jack.so
%dir %{_datadir}/obs/obs-plugins/linux-jack
%dir %{_datadir}/obs/obs-plugins/linux-jack/locale
%endif
%{_libdir}/obs-plugins/linux-pipewire.so
%{_libdir}/obs-plugins/linux-pulseaudio.so
%{_libdir}/obs-plugins/linux-v4l2.so
%{_libdir}/obs-plugins/obs-ffmpeg.so
%{_libdir}/obs-plugins/obs-filters.so
%{_libdir}/obs-plugins/obs-nvenc.so
%{_libdir}/obs-plugins/obs-outputs.so
%ifarch %{x8664} x32
%{_libdir}/obs-plugins/obs-qsv11.so
%dir %{_datadir}/obs/obs-plugins/obs-qsv11
%dir %{_datadir}/obs/obs-plugins/obs-qsv11/locale
%endif
%{_libdir}/obs-plugins/obs-transitions.so
%{_libdir}/obs-plugins/obs-vst.so
%{_libdir}/obs-plugins/obs-x264.so
%{_libdir}/obs-plugins/rtmp-services.so
%{_libdir}/obs-plugins/text-freetype2.so
%{_libdir}/obs-plugins/vlc-video.so
%dir %{_libdir}/obs-scripting
%ifnarch x32
%{_libdir}/obs-scripting/obslua.so
%endif
%{_libdir}/obs-scripting/_obspython.so
%attr(755,root,root) %{_libdir}/obs-scripting/obspython.py

%{_datadir}/metainfo/com.obsproject.Studio.metainfo.xml
%{_desktopdir}/com.obsproject.Studio.desktop
%{_iconsdir}/hicolor/*x*/apps/com.obsproject.Studio.png
%{_iconsdir}/hicolor/scalable/apps/com.obsproject.Studio.svg

%dir %{_datadir}/obs
%{_datadir}/obs/libobs
%dir %{_datadir}/obs/obs-plugins
%dir %{_datadir}/obs/obs-studio
%{_datadir}/obs/obs-studio/OBSPublicRSAKey.pem
%{_datadir}/obs/obs-studio/authors
%{_datadir}/obs/obs-studio/images
%{_datadir}/obs/obs-studio/license
%dir %{_datadir}/obs/obs-studio/locale
%{_datadir}/obs/obs-studio/themes
%{_datadir}/obs/obs-studio/locale.ini
%{_datadir}/obs/obs-studio/striped_line.effect

%dir %{_datadir}/obs/obs-plugins/decklink
%dir %{_datadir}/obs/obs-plugins/decklink/locale

%dir %{_datadir}/obs/obs-plugins/frontend-tools
%dir %{_datadir}/obs/obs-plugins/frontend-tools/locale
%dir %{_datadir}/obs/obs-plugins/frontend-tools/scripts
%{_datadir}/obs/obs-plugins/frontend-tools/scripts/*.lua
%{_datadir}/obs/obs-plugins/frontend-tools/scripts/*.py
%{_datadir}/obs/obs-plugins/frontend-tools/scripts/clock-source

%dir %{_datadir}/obs/obs-plugins/image-source
%dir %{_datadir}/obs/obs-plugins/image-source/locale

%dir %{_datadir}/obs/obs-plugins/linux-alsa
%dir %{_datadir}/obs/obs-plugins/linux-alsa/locale

%dir %{_datadir}/obs/obs-plugins/linux-capture
%dir %{_datadir}/obs/obs-plugins/linux-capture/locale

%dir %{_datadir}/obs/obs-plugins/linux-pipewire
%dir %{_datadir}/obs/obs-plugins/linux-pipewire/locale

%dir %{_datadir}/obs/obs-plugins/linux-pulseaudio
%dir %{_datadir}/obs/obs-plugins/linux-pulseaudio/locale

%dir %{_datadir}/obs/obs-plugins/linux-v4l2
%dir %{_datadir}/obs/obs-plugins/linux-v4l2/locale

%dir %{_datadir}/obs/obs-plugins/obs-ffmpeg
%dir %{_datadir}/obs/obs-plugins/obs-ffmpeg/locale

%dir %{_datadir}/obs/obs-plugins/obs-filters
%{_datadir}/obs/obs-plugins/obs-filters/*.effect
%{_datadir}/obs/obs-plugins/obs-filters/LUTs
%dir %{_datadir}/obs/obs-plugins/obs-filters/locale

%dir %{_datadir}/obs/obs-plugins/obs-nvenc
%dir %{_datadir}/obs/obs-plugins/obs-nvenc/locale

%dir %{_datadir}/obs/obs-plugins/obs-outputs
%dir %{_datadir}/obs/obs-plugins/obs-outputs/locale

%dir %{_datadir}/obs/obs-plugins/obs-transitions
%{_datadir}/obs/obs-plugins/obs-transitions/*.effect
%{_datadir}/obs/obs-plugins/obs-transitions/luma_wipes
%dir %{_datadir}/obs/obs-plugins/obs-transitions/locale

%dir %{_datadir}/obs/obs-plugins/obs-vst
%dir %{_datadir}/obs/obs-plugins/obs-vst/locale

%dir %{_datadir}/obs/obs-plugins/obs-x264
%dir %{_datadir}/obs/obs-plugins/obs-x264/locale

%dir %{_datadir}/obs/obs-plugins/rtmp-services
%{_datadir}/obs/obs-plugins/rtmp-services/*.json
%dir %{_datadir}/obs/obs-plugins/rtmp-services/schema
%{_datadir}/obs/obs-plugins/rtmp-services/schema/*.json
%dir %{_datadir}/obs/obs-plugins/rtmp-services/locale

%dir %{_datadir}/obs/obs-plugins/text-freetype2
%{_datadir}/obs/obs-plugins/text-freetype2/*.effect
%dir %{_datadir}/obs/obs-plugins/text-freetype2/locale

%dir %{_datadir}/obs/obs-plugins/vlc-video
%dir %{_datadir}/obs/obs-plugins/vlc-video/locale

%files devel
%defattr(644,root,root,755)
%{_libdir}/libobs.so
%{_libdir}/libobs-frontend-api.so
%{_libdir}/libobs-opengl.so
%{_libdir}/libobs-scripting.so
%{_includedir}/obs
%{_pkgconfigdir}/libobs.pc
%{_pkgconfigdir}/obs-frontend-api.pc
%{_libdir}/cmake/libobs
%{_libdir}/cmake/obs-frontend-api
