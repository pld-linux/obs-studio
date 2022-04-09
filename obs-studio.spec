Summary:	OBS Studio - live streaming and screen recording software
Summary(pl.UTF-8):	OBS Studio - oprogramowanie do przesyłania strumieni na żywo i nagrywania ekranu
Name:		obs-studio
Version:	27.2.4
Release:	4
License:	GPL v2+
%define		obs_vst_gitref	8ad3f64e702ac4f1799b209a511620eb1d096a01
Group:		X11/Applications/Multimedia
#Source0Download: https://github.com/obsproject/obs-studio/releases
Source0:	https://github.com/jp9000/obs-studio/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	a79f8bf28ab9995e333fc1ac0bcfa708
Source1:	https://github.com/obsproject/obs-vst/archive/%{obs_vst_gitref}/obs-vst-20220206.tar.gz
# Source1-md5:	7554389796e176c6bc73d453cf883703
Patch0:		mbedtls3-compatibility.patch
Patch1:		Remove_encrypted_RTMP_support.patch
URL:		https://obsproject.com/
BuildRequires:	ImageMagick-devel
BuildRequires:	OpenGL-GLX-devel
BuildRequires:	Qt5Core-devel >= 5
BuildRequires:	Qt5Gui-devel >= 5
BuildRequires:	Qt5Svg-devel >= 5
BuildRequires:	Qt5Widgets-devel >= 5
BuildRequires:	Qt5X11Extras-devel >= 5
BuildRequires:	alsa-lib-devel
BuildRequires:	cmake >= 2.8.12
BuildRequires:	curl-devel
BuildRequires:	dbus-devel
BuildRequires:	fdk-aac-devel
# avcodec avfilter avdevice avutil swscale avformat swresample
BuildRequires:	ffmpeg-devel
BuildRequires:	fontconfig-devel
BuildRequires:	freetype-devel >= 2
BuildRequires:	jack-audio-connection-kit-devel
BuildRequires:	jansson-devel >= 2.5
BuildRequires:	libv4l-devel
BuildRequires:	libxcb-devel
%ifnarch x32
BuildRequires:	luajit-devel
%endif
BuildRequires:	libstdc++-devel >= 6:4.7
BuildRequires:	libx264-devel
BuildRequires:	mbedtls-devel
BuildRequires:	pipewire-devel
BuildRequires:	pkgconfig
BuildRequires:	pulseaudio-devel
BuildRequires:	python3-devel >= 1:3.2
BuildRequires:	qt5-build >= 5
BuildRequires:	qt5-qmake >= 5
BuildRequires:	speexdsp-devel
BuildRequires:	swig-python >= 2
BuildRequires:	udev-devel
BuildRequires:	vlc-devel
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	zlib-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_noautoprovfiles	%{_libdir}/obs-plugins

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
%setup -q -a1
%patch0 -p1
%patch1 -p1
%{__mv} obs-vst-%{obs_vst_gitref} obs-vst
%{__mv} obs-vst plugins

%build
install -d build
cd build

export OBS_MULTIARCH_SUFFIX="%(echo "%{_lib}" | sed -e 's/^lib//')"
%cmake .. \
	-DUNIX_STRUCTURE=1 \
	-DOBS_VERSION_OVERRIDE=%{version} \
	-DBUILD_BROWSER=OFF

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install/fast \
        DESTDIR=$RPM_BUILD_ROOT

builddir="$(pwd)"

cd $RPM_BUILD_ROOT
reldatadir="$(echo %{_datadir} | sed -e 's,^/,,')"
for f in $reldatadir/obs/obs-studio/locale/??*-??*.ini $reldatadir/obs/obs-plugins/*/locale/??*-??*.ini ; do
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
%{__rm} $RPM_BUILD_ROOT%{_datadir}/obs/obs-plugins/{decklink-captions,decklink-ouput-ui}/.keepme

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS README.rst
%attr(755,root,root) %{_bindir}/obs
%attr(755,root,root) %{_bindir}/obs-ffmpeg-mux
%attr(755,root,root) %{_libdir}/libobs-frontend-api.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libobs-frontend-api.so.0
%attr(755,root,root) %{_libdir}/libobs-opengl.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libobs-opengl.so.0
%attr(755,root,root) %{_libdir}/libobs.so.0
%attr(755,root,root) %{_libdir}/libobsglad.so.0
%attr(755,root,root) %{_libdir}/libobs-scripting.so

%dir %{_libdir}/obs-plugins
%attr(755,root,root) %{_libdir}/obs-plugins/decklink-captions.so
%attr(755,root,root) %{_libdir}/obs-plugins/decklink-ouput-ui.so
%attr(755,root,root) %{_libdir}/obs-plugins/frontend-tools.so
%attr(755,root,root) %{_libdir}/obs-plugins/image-source.so
%attr(755,root,root) %{_libdir}/obs-plugins/linux-alsa.so
%attr(755,root,root) %{_libdir}/obs-plugins/linux-capture.so
%attr(755,root,root) %{_libdir}/obs-plugins/linux-decklink.so
%attr(755,root,root) %{_libdir}/obs-plugins/linux-jack.so
%attr(755,root,root) %{_libdir}/obs-plugins/linux-pulseaudio.so
%attr(755,root,root) %{_libdir}/obs-plugins/linux-v4l2.so
%attr(755,root,root) %{_libdir}/obs-plugins/obs-ffmpeg.so
%attr(755,root,root) %{_libdir}/obs-plugins/obs-filters.so
%attr(755,root,root) %{_libdir}/obs-plugins/obs-libfdk.so
%attr(755,root,root) %{_libdir}/obs-plugins/obs-outputs.so
%attr(755,root,root) %{_libdir}/obs-plugins/obs-transitions.so
%attr(755,root,root) %{_libdir}/obs-plugins/obs-vst.so
%attr(755,root,root) %{_libdir}/obs-plugins/obs-x264.so
%attr(755,root,root) %{_libdir}/obs-plugins/rtmp-services.so
%attr(755,root,root) %{_libdir}/obs-plugins/text-freetype2.so
%attr(755,root,root) %{_libdir}/obs-plugins/vlc-video.so
%dir %{_libdir}/obs-scripting
%ifnarch x32
%attr(755,root,root) %{_libdir}/obs-scripting/obslua.so
%endif
%attr(755,root,root) %{_libdir}/obs-scripting/_obspython.so
%attr(755,root,root) %{_libdir}/obs-scripting/obspython.py

%{_datadir}/metainfo/com.obsproject.Studio.appdata.xml
%{_desktopdir}/com.obsproject.Studio.desktop
%{_iconsdir}/hicolor/*x*/apps/com.obsproject.Studio.png
%{_iconsdir}/hicolor/scalable/apps/com.obsproject.Studio.svg

%dir %{_datadir}/obs
%{_datadir}/obs/libobs
%dir %{_datadir}/obs/obs-plugins
%dir %{_datadir}/obs/obs-studio
%{_datadir}/obs/obs-studio/authors
%{_datadir}/obs/obs-studio/images
%{_datadir}/obs/obs-studio/license
%dir %{_datadir}/obs/obs-studio/locale
%{_datadir}/obs/obs-studio/themes
%{_datadir}/obs/obs-studio/locale.ini

%dir %{_datadir}/obs/obs-plugins/decklink-ouput-ui

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

%dir %{_datadir}/obs/obs-plugins/linux-decklink
%dir %{_datadir}/obs/obs-plugins/linux-decklink/locale

%dir %{_datadir}/obs/obs-plugins/linux-jack
%dir %{_datadir}/obs/obs-plugins/linux-jack/locale

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

%dir %{_datadir}/obs/obs-plugins/obs-libfdk
%dir %{_datadir}/obs/obs-plugins/obs-libfdk/locale

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
%dir %{_datadir}/obs/obs-plugins/rtmp-services/locale

%dir %{_datadir}/obs/obs-plugins/text-freetype2
%{_datadir}/obs/obs-plugins/text-freetype2/*.effect
%dir %{_datadir}/obs/obs-plugins/text-freetype2/locale

%dir %{_datadir}/obs/obs-plugins/vlc-video
%dir %{_datadir}/obs/obs-plugins/vlc-video/locale

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libobs.so
%attr(755,root,root) %{_libdir}/libobs-frontend-api.so
%attr(755,root,root) %{_libdir}/libobs-opengl.so
%attr(755,root,root) %{_libdir}/libobsglad.so
%{_includedir}/obs
%{_pkgconfigdir}/libobs.pc
%{_libdir}/cmake/LibObs
