#
# NOTE: the package is prepared mainly for Asterisk needs, so it is configured
# the way Asterisk wiki suggests:
# https://wiki.asterisk.org/wiki/display/AST/Building+and+Installing+pjproject
#
# If we have another package using this library we may need to change bcond
# defaults.
#
# TODO:
#	- fix --with opencore_amr
# 	- libresample.so conflicts with the libresample-devel package
#

# Conditional build:
%bcond_with	sound		# enable sound support (AST wiki suggests disabling it)
%bcond_with	video		# enable video support (AST wiki suggests disabling it)
%bcond_with	resample	# enable resample support (AST wiki suggests disabling it)
%bcond_with	opencore_amr	# enable opencore-arm support (AST wiki suggests disabling it)

Summary:	PJSIP - free and open source multimedia communication library
Name:		pjproject
Version:	2.3
Release:	4
License:	GPL v2+
Group:		Libraries
Source0:	http://www.pjsip.org/release/%{version}/%{name}-%{version}.tar.bz2
# Source0-md5:	8440e43242c439ae5ec30b5b85005fce
Patch0:		%{name}-ilbc-link.patch
URL:		http://www.pjsip.org/
%{?with_video:BuildRequires:	SDL2-devel}
BuildRequires:	SILK_SDK-devel
BuildRequires:	autoconf
%{?with_video:BuildRequires:	ffmpeg-devel}
BuildRequires:	libgsm-devel
%{?with_video:BuildRequires:	libv4l-devel}
%{?with_opencore_amr:BuildRequires:	opencore-amr-devel}
BuildRequires:	openssl-devel
BuildRequires:	pkgconfig
%{?with_sound:BuildRequires:	portaudio-devel}
BuildRequires:	python-modules
BuildRequires:	rpmbuild(macros) >= 1.583
BuildRequires:	speex-devel
BuildRequires:	speexdsp-devel
BuildRequires:	srtp-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# dependency loop between libpjmedia-videodev.so and libpjmedia.so
%define		skip_post_check_so	libpjmedia-videodev.so.*

%ifarch x32
%define		libsuffix	x86_64-pld-linux-gnux32
%else
%define		libsuffix	%{_arch}-pld-linux-gnu
%endif

%description
PJSIP is a free and open source multimedia communication library
written in C language implementing standard based protocols such as
SIP, SDP, RTP, STUN, TURN, and ICE. It combines signaling protocol
(SIP) with rich multimedia framework and NAT traversal functionality
into high level API that is portable and suitable for almost any type
of systems ranging from desktops, embedded systems, to mobile
handsets.

PJSIP is both compact and feature rich. It supports audio, video,
presence, and instant messaging, and has extensive documentation.
PJSIP is very portable. On mobile devices, it abstracts system
dependent features and in many cases is able to utilize the native
multimedia capabilities of the device.

%package devel
Summary:	Header files for %{name} library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki %{name}
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	SILK_SDK-devel

%description devel
Header files for %{name} library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki %{name}.

%package static
Summary:	Static %{name} library
Summary(pl.UTF-8):	Statyczna biblioteka %{name}
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static %{name} library.

%description static -l pl.UTF-8
Statyczna biblioteka %{name}.

%prep
%setup -q
%patch0 -p1

%build
%{__autoconf} -o configure aconfigure.ac

%configure \
	CFLAGS="%{rpmcflags} %{?with_video:-DPJMEDIA_HAS_VIDEO=1}" \
	--enable-shared \
	%{__enable_disable sound sound} \
	%{__enable_disable video video} \
	%{__enable_disable resample resample} \
	%{__enable_disable opencore_amr opencore-amr} \
	%{__with sound external-pa} \
	--without-libyuv \
	--disable-libyuv \
	--with-external-speex \
	--with-external-srtp \
	--with-external-gsm
%{__make} -j1

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -j1 install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README.txt
%attr(755,root,root) %{_libdir}/libg7221codec.so.2
%attr(755,root,root) %{_libdir}/libilbccodec.so.2
%attr(755,root,root) %{_libdir}/libpj.so.2
%attr(755,root,root) %{_libdir}/libpjlib-util.so.2
%attr(755,root,root) %{_libdir}/libpjmedia-audiodev.so.2
%attr(755,root,root) %{_libdir}/libpjmedia-codec.so.2
%attr(755,root,root) %{_libdir}/libpjmedia-videodev.so.2
%attr(755,root,root) %{_libdir}/libpjmedia.so.2
%attr(755,root,root) %{_libdir}/libpjnath.so.2
%attr(755,root,root) %{_libdir}/libpjsip-simple.so.2
%attr(755,root,root) %{_libdir}/libpjsip-ua.so.2
%attr(755,root,root) %{_libdir}/libpjsip.so.2
%attr(755,root,root) %{_libdir}/libpjsua.so.2
%attr(755,root,root) %{_libdir}/libpjsua2.so.2
%{?with_resample:%attr(755,root,root) %{_libdir}/libresample.so.2}

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libg7221codec.so
%attr(755,root,root) %{_libdir}/libilbccodec.so
%attr(755,root,root) %{_libdir}/libpj.so
%attr(755,root,root) %{_libdir}/libpjlib-util.so
%attr(755,root,root) %{_libdir}/libpjmedia-audiodev.so
%attr(755,root,root) %{_libdir}/libpjmedia-codec.so
%attr(755,root,root) %{_libdir}/libpjmedia-videodev.so
%attr(755,root,root) %{_libdir}/libpjmedia.so
%attr(755,root,root) %{_libdir}/libpjnath.so
%attr(755,root,root) %{_libdir}/libpjsip-simple.so
%attr(755,root,root) %{_libdir}/libpjsip-ua.so
%attr(755,root,root) %{_libdir}/libpjsip.so
%attr(755,root,root) %{_libdir}/libpjsua.so
%attr(755,root,root) %{_libdir}/libpjsua2.so
%{?with_resample:%attr(755,root,root) %{_libdir}/libresample.so}
%{_includedir}/pj*
%{_pkgconfigdir}/lib%{name}.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libg7221codec-%{libsuffix}.a
%{_libdir}/libilbccodec-%{libsuffix}.a
%{_libdir}/libpj-%{libsuffix}.a
%{_libdir}/libpjlib-util-%{libsuffix}.a
%{_libdir}/libpjmedia-audiodev-%{libsuffix}.a
%{_libdir}/libpjmedia-codec-%{libsuffix}.a
%{_libdir}/libpjmedia-%{libsuffix}.a
%{_libdir}/libpjmedia-videodev-%{libsuffix}.a
%{_libdir}/libpjnath-%{libsuffix}.a
%{_libdir}/libpjsip-%{libsuffix}.a
%{_libdir}/libpjsip-simple-%{libsuffix}.a
%{_libdir}/libpjsip-ua-%{libsuffix}.a
%{_libdir}/libpjsua-%{libsuffix}.a
%{_libdir}/libpjsua2-%{libsuffix}.a
%{?with_resample:%{_libdir}/libresample-%{libsuffix}.a}
