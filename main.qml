import QtQuick.Window 2.2 //2.1
import QtQuick.Controls 1.4 //1.4
import QtQuick.Controls.Styles 1.4
import QtQuick.Extras 1.4
import QtQuick.Controls.Styles.Desktop 1.0
import QtQuick 2.12//2.12
import QtQuick.Window 2.12
import QtQuick.Controls 2.0
import QtQuick.Layouts 1.1
import QtLocation 5.11
import QtPositioning 5.0
import QtQuick.Window 2.3
import QtGraphicalEffects 1.0
import QtQuick.Controls.Imagine 2.3
import QtQuick.Controls.Material 2.0
import QtQuick 2.7

import QtQuick 2.12
import QtQuick.Window 2.13
import QtQuick.Controls 2.3
import QtQuick.Controls.Styles 1.4
import QtQuick.Extras 1.4
import QtQuick.Extras.Private 1.0

//import QtQuick.Window 2.2
import QtQuick 2.9
import QtCharts 2.1


Window {
	
	id : root
	x : 30
	y : 30
	width: 1300
	maximumWidth : 1300
	minimumWidth : 1300
    height: 700
	maximumHeight : 700
	minimumHeight : 700
	title:"2D DPS CONTROLLER SIMULATOR"
	color : "#147CA6"
    visible: true

	property real sp_lat_val: -6.215861 // Variabel latitude
    property real sp_lon_val: 107.803706 // Variabel longitude
	
	property real lat_p1: 0
	property real long_p1: 0
	
	property real lat_p2: 0
	property real long_p2: 0
	
	property real lat_p3: 0
	property real long_p3: 0
	
	property var state
	
	function updateAxis() {
				var arr = [cv.valueCH1, cv.valueCH2, cv.valueCH3]

				var minVal = Math.min(arr[0], arr[1], arr[2])
				var maxVal = Math.max(arr[0], arr[1], arr[2])

				// Tambah gap 0.1
				yAxis1.min = minVal - 0.1
				yAxis1.max = maxVal + 0.1
			}

	function upload_csv() {
		console.log("uploading csv....")
		markerModel.clear()
		md.clear()
		//backend.line_reset(0)
			   
		for (var index = li.pathLength(); index >= 0; index--){
            li.removeCoordinate([index]);
            //li1.removeCoordinate([index]);
                                    
        }

        for (var i = 0; i < rpl_lat.length; i++) {
		
			var coordinate = QtPositioning.coordinate(rpl_lat[i], rpl_long[i]);
			markerModel.append({"latitude": rpl_lat[i], "longitude": rpl_long[i]});
			var text = md.count + 1;
			md.append({"coords": coordinate, "title": text});
			li.addCoordinate(coordinate)

		}

	}
	
	
	function updateChart() {
		var deg = backend.deg()
		var val = backend.val()

		seriespolar1.clear()

		for (var i = 0; i < deg.length; i++) {
			seriespolar1.append(deg[i], val[i])
		}
	}
	

	


	Text {
		x : 620
		y : 680
		width: 83
		height: 21
		color: "white"
		text: "(c) Muhammad Husni Muttaqin 23223303"
		font.pixelSize: 14
		horizontalAlignment: Text.AlignHCenter
		verticalAlignment: Text.AlignVCenter
		font.family: "Verdana"
		font.bold: true
	}



	Rectangle{
		x : 950
		color : "transparent"
		border.width : 3
		border.color : "white"
		height : 650
		width : 250
		visible : false

	Text {
                id : starting_point
                x: 10
                y: 350
                width: 83
                height: 21
                color: "white"
                text: "starting point :"
                font.pixelSize: 14
                horizontalAlignment: Text.AlignLeft
                verticalAlignment: Text.AlignTop
                font.family: "Verdana"
                font.bold: true
				visible : true
            }



	Button {
           id : set_button
            x: 10
            y: 400
            text : "MPC RUN"
			width: 170
            //height: 31
            checkable: true
            checked: false
           
		   onClicked:{
					
						
						//backend.setpoint(sp_lat.text, sp_lon.text, sp_yaw.text)
						//starting_point.text = sp_lat.text+","+sp_lon.text+","+sp_yaw.text
					
					}
			
        }
	
	
	Button {
           id : pop
            x: 10
            y: 450
            text : "pop"
			width: 170
            //height: 31
            checkable: false
            checked: false
			
			onClicked:{
				backend.pop("hehe")
			}
			
	}
	Timer{
		id:mpc_run
		interval: 2000
		repeat: true
		running: true//set_button.checked
		onTriggered: {
			//backend.animate("tick")
			backend.setpoint(sp_lat.text, sp_lon.text, sp_yaw.text)
		}

	}		
	
	


	Text {
		anchors.horizontalCenter: parent.horizontalCenter
		y : 20
		width: 83
		height: 21
		color: "white"
		text: "2D DPS CONTROLLER\nSIMULATOR"
		font.pixelSize: 14
		horizontalAlignment: Text.AlignHCenter
		verticalAlignment: Text.AlignVCenter
		font.family: "Verdana"
		font.bold: true
	}
			
	Text {
                
                x: 10
                y: 50
                width: 83
                height: 21
                color: "white"
                text: "Setpoint"
                font.pixelSize: 14
                horizontalAlignment: Text.AlignLeft
                verticalAlignment: Text.AlignTop
                font.family: "Verdana"
                font.bold: true
            }
			
	Text{
					id : sp_lat
					x : 60
					y : 80
					text : "-6.215861"
					width : 120
					color: "white"
					
					Text{
						//anchors.horizontalCenter: parent.horizontalCenter
						x : -50
						y:10
						text:"lat : "
						color : "white"
						font.family: "Cantora One"  // Set the font family
						font.pixelSize: 15    // Set the font size
						font.bold: true 
					}
				}
				
	Text{
					id : sp_lon
					x : 60
					y : 120
					text : "107.803706"
					width : 120
					color: "white"
					
					Text{
						//anchors.horizontalCenter: parent.horizontalCenter
						x : -50
						y:10
						text:"lon : "
						color : "white"
						font.family: "Cantora One"  // Set the font family
						font.pixelSize: 15    // Set the font size
						font.bold: true 
					}
				}
				
	Text{
					id : sp_yaw
					x : 60
					y : 160
					text : "0"
					width : 120
					color: "white"
					
					Text{
						//anchors.horizontalCenter: parent.horizontalCenter
						x : -50
						y:10
						text:"yaw : "
						color : "white"
						font.family: "Cantora One"  // Set the font family
						font.pixelSize: 15    // Set the font size
						font.bold: true 
					}
				}
			
			
			
			
	Text {
                
                x: 10
                y: 220
                width: 83
                height: 21
                color: "white"
                text: "DISTURBANCE :"
                font.pixelSize: 14
                horizontalAlignment: Text.AlignLeft
                verticalAlignment: Text.AlignTop
                font.family: "Verdana"
                font.bold: true
            }
			
			
	TextField{
					id : wind_speed
					x : 90
					y : 250
					text : "1"
					width : 120
					
					Text{
						//anchors.horizontalCenter: parent.horizontalCenter
						x : -80
						y:10
						text:"wind speed : "
						color : "white"
						font.family: "Cantora One"  // Set the font family
						font.pixelSize: 15    // Set the font size
						font.bold: true 
					}
				}
				
	TextField{
					id : wind_dir
					x : 90
					y : 300
					text :"90"
					width : 120
					
					Text{
						//anchors.horizontalCenter: parent.horizontalCenter
						x : -80
						y:10
						text:"wind dir : "
						color : "white"
						font.family: "Cantora One"  // Set the font family
						font.pixelSize: 15    // Set the font size
						font.bold: true 
					}
				}
			
	
	
	
	


	
	
	Button {
            id: controller_setup
            x: 10
            y: 90
            text : "controller setup"
			//width: 34
            //height: 31
            checkable: false
            checked: false
			visible : false
		   onClicked:{
						
					}
			
        }
 

}


	Rectangle{
		x : 880
		color : "transparent"
		border.width : 3
		border.color : "white"
		height : 350
		width : 400
		visible : true
		
		Rectangle{
					x : 0
					y : 80
					height : 250
					width : 400
					color : "transparent"
					border.width : 3
					border.color : "transparent"
					
		Rectangle{
					x : 180
					y : 0
					width : 200
					height : 75
					color : "transparent"
					border.width : 3
					border.color : "transparent"
					
					Text {
							//anchors.horizontalCenter: parent.horizontalCenter
							x:80
							y: 10
							color: "white"
							text: "Propeller 1"
							font.pixelSize: 14
							horizontalAlignment: Text.AlignLeft
							verticalAlignment: Text.AlignTop
							font.family: "Verdana"
							font.bold: true
						}
					
					Image{
						id : azimuth1
						//anchors.horizontalCenter: parent.horizontalCenter
						x: 0
						y : 0
						width : 120
						height : 80
						source: "needlewhite.png"
						transformOrigin: Item.Center
						visible :true
						opacity : 0.5
						rotation: 180
						scale: 1
					}
					
					
					Image{
						id : azimuth1_real
						//anchors.horizontalCenter: parent.horizontalCenter
						x: 0
						y : 0
						width : 120
						height : 80
						source: "needle.png"
						transformOrigin: Item.Center
						visible :true
						
						rotation: 0
						scale: 1
					}
					
					Text {
							//anchors.horizontalCenter: parent.horizontalCenter
							x:80
							id : properties1
							y: 30
							color: "white"
							text: "properties"
							font.pixelSize: 14
							horizontalAlignment: Text.AlignLeft
							verticalAlignment: Text.AlignTop
							font.family: "Verdana"
							
						}
						
					Text {
							//anchors.horizontalCenter: parent.horizontalCenter
							x:80
							id : properties1_real
							y: 50
							color: "red"
							text: "properties"
							font.pixelSize: 14
							horizontalAlignment: Text.AlignLeft
							verticalAlignment: Text.AlignTop
							font.family: "Verdana"
							
						}
					
					
				
				}

				Rectangle{
					x : 180
					y : 150
					width : 200
					height : 75
					color : "transparent"
					border.width : 3
					border.color : "transparent"
					
					Text {
							//anchors.horizontalCenter: parent.horizontalCenter
							
							x: 80
							y: 10
							color: "white"
							text: "Propeller 2"
							font.pixelSize: 14
							horizontalAlignment: Text.AlignLeft
							verticalAlignment: Text.AlignTop
							font.family: "Verdana"
							font.bold: true
						}
						
						
					Image{
						id : azimuth2
						//anchors.horizontalCenter: parent.horizontalCenter
						x : 0
						y : 0
						width : 120
						height : 80
						source: "needlewhite.png"
						transformOrigin: Item.Center
						visible :true
						opacity : 0.5
						
						rotation: 180
						scale: 1
					}
					
					
					Image{
						id : azimuth2_real
						//anchors.horizontalCenter: parent.horizontalCenter
						x : 0
						y : 0
						width : 120
						height : 80
						source: "needle.png"
						transformOrigin: Item.Center
						visible :true
						
						rotation: 180
						scale: 1
					}
					
					Text {
							//anchors.horizontalCenter: parent.horizontalCenter
							id : properties2
							x : 80
							y: 30
							color: "white"
							text: "properties"
							font.pixelSize: 14
							horizontalAlignment: Text.AlignLeft
							verticalAlignment: Text.AlignTop
							font.family: "Verdana"
							
						}
						
					Text {
							//anchors.horizontalCenter: parent.horizontalCenter
							id : properties2_real
							x : 80
							y: 50
							color: "red"
							text: "properties"
							font.pixelSize: 14
							horizontalAlignment: Text.AlignLeft
							verticalAlignment: Text.AlignTop
							font.family: "Verdana"
							
						}
					
					
				
				}



				Rectangle{
					x : 0
					y : 150
					width : 200
					height : 75
					color : "transparent"
					border.width : 3
					border.color : "transparent"
					
					Text {
							//anchors.horizontalCenter: parent.horizontalCenter
							x: 10
							y: 10
							color: "white"
							text: "Propeller 3"
							font.pixelSize: 14
							horizontalAlignment: Text.AlignLeft
							verticalAlignment: Text.AlignTop
							font.family: "Verdana"
							font.bold: true
						}
						
					Image{
						id : azimuth3
						//anchors.horizontalCenter: parent.horizontalCenter
						x : 100
						y : 0
						width : 120
						height : 80
						source: "needlewhite.png"
						transformOrigin: Item.Center
						opacity : 0.5
						visible :true
						
						rotation: 180
						scale: 1
					}
					
					Image{
						id : azimuth3_real
						//anchors.horizontalCenter: parent.horizontalCenter
						x : 100
						y : 0
						width : 120
						height : 80
						source: "needle.png"
						transformOrigin: Item.Center
						visible :true
						
						rotation: 180
						scale: 1
					}
					
					
					Text {
							//anchors.horizontalCenter: parent.horizontalCenter
							x : 10
							id : properties3
							y: 30
							color: "white"
							text: "properties"
							font.pixelSize: 14
							horizontalAlignment: Text.AlignLeft
							verticalAlignment: Text.AlignTop
							font.family: "Verdana"
							
						}
						
					Text {
							//anchors.horizontalCenter: parent.horizontalCenter
							x : 10
							id : properties3_real
							y: 50
							color: "red"
							text: "properties"
							font.pixelSize: 14
							horizontalAlignment: Text.AlignLeft
							verticalAlignment: Text.AlignTop
							font.family: "Verdana"
							
						}
					
					
				
				}



				Rectangle{
					x : 0
					y : 0
					width : 200
					height : 75
					color : "transparent"
					border.width : 3
					border.color : "transparent"
					
					Text {
							//anchors.horizontalCenter: parent.horizontalCenter
							
							x: 10
							y: 10
							color: "white"
							text: "Propeller 4"
							font.pixelSize: 14
							horizontalAlignment: Text.AlignLeft
							verticalAlignment: Text.AlignTop
							font.family: "Verdana"
							font.bold: true
						}
						
					Rectangle{
					x : 100
						//y : 20
					width : 120
					height : 80
					color : "transparent"
					border.width : 3
					border.color : "Transparent"
					radius : width/2
					

					
					Image{
						id : azimuth4
						//anchors.horizontalCenter: parent.horizontalCenter
						x : 0
						//y : 20
						width : 120
						height : 80
						source: "needlewhite.png"
						transformOrigin: Item.Center
						visible :true
						opacity: 0.5
						
						rotation: 180
						scale: 1
					}
					
					
					Image{
						id : azimuth4_real
						//anchors.horizontalCenter: parent.horizontalCenter
						x : 0
						//y : 20
						width : 120
						height : 80
						source: "needle.png"
						transformOrigin: Item.Center
						visible :true
						
						rotation: 180
						scale: 1
					}
					
					}
					
					Text {
							//anchors.horizontalCenter: parent.horizontalCenter
							id : properties4
							x :10
							y: 30
							color: "white"
							text: "properties"
							font.pixelSize: 14
							horizontalAlignment: Text.AlignLeft
							verticalAlignment: Text.AlignTop
							font.family: "Verdana"
							
						}
						
					Text {
							//anchors.horizontalCenter: parent.horizontalCenter
							id : properties4_real
							x :10
							y: 50
							color: "red"
							text: "properties"
							font.pixelSize: 14
							horizontalAlignment: Text.AlignLeft
							verticalAlignment: Text.AlignTop
							font.family: "Verdana"
							
						}
					
					
				
				}
		
		// ICON KAPAL DI TENGAH
    Canvas {
		id : ship_icon
		y : parent.width/10
        width: Math.min(parent.width, parent.height)/5
        height: Math.min(parent.width, parent.height)/1
        anchors.centerIn: parent

        onPaint: {
			
			    var ctx = getContext("2d")
				ctx.clearRect(0, 0, width, height)

				var yOffset = 10   // geser ke bawah (+), ke atas (-)

				ctx.beginPath()

				ctx.moveTo(width/2, 0 + yOffset)

				ctx.lineTo(width, height*0.15 + yOffset)
				ctx.lineTo(width, height*0.75 + yOffset)

				ctx.lineTo(0, height*0.75 + yOffset)

				ctx.lineTo(0, height*0.15 + yOffset)

				ctx.closePath()
				
				// isi warna putih
				ctx.fillStyle = "white"
				ctx.fill()

				ctx.strokeStyle = "black"
				ctx.lineWidth = 4
				ctx.stroke()
			
        }
    }
	
		}
		
		
	}


	Rectangle{
		x : 880
		y : 350
		color : "transparent"
		border.width : 3
		border.color : "white"
		height : 350
		width : 400
		visible : true
		
	PolarChartView {
	id : polar_chart 
    title: "Vessel Capabilty Plot"
    anchors.fill: parent
    legend.visible: false
    antialiasing: true

    ValueAxis {
        id: axisAngular
        min: 0
        max: 360
        tickCount: 9
    }

    ValueAxis {
        id: axisRadial
        min: 0
        max: 45
    }

    SplineSeries {
        id: seriespolar1
        axisAngular: axisAngular
        axisRadial: axisRadial
        pointsVisible: false
		
    }
	
	

    // Add data dynamically to the series
    
	
	// Timer update tiap 1 detik
    Timer {
        interval: 1000   // 1000 ms = 1 detik
        running: true
        repeat: true

        onTriggered: {
            
			//backend.tick(1)
			//console.log(Math.min(polar_chart.width, polar_chart.height))
			//console.log("tick")
			backend.tick(1)
			
			updateChart()
			
			//console.log(backend.val())
		}
    }
}
	
	
	Canvas {
		id : ship_icon2
		y : parent.width/10
        width: Math.min(polar_chart.width, polar_chart.height)/20
        height: Math.min(polar_chart.width, polar_chart.height)/5
        anchors.centerIn: parent

        onPaint: {
			
			    var ctx = getContext("2d")
				ctx.clearRect(0, 0, width, height)

				var yOffset = 10   // geser ke bawah (+), ke atas (-)

				ctx.beginPath()

				ctx.moveTo(width/2, 0 + yOffset)

				ctx.lineTo(width, height*0.15 + yOffset)
				ctx.lineTo(width, height*0.75 + yOffset)

				ctx.lineTo(0, height*0.75 + yOffset)

				ctx.lineTo(0, height*0.15 + yOffset)

				ctx.closePath()

				ctx.strokeStyle = "black"
				ctx.lineWidth = 4
				ctx.stroke()
			
        }
    }
	
		
	}

	Rectangle{
		x : 525
		color : "transparent"
		border.width : 3
		border.color : "white"
		height : 530
		width : 350
		
		ScrollView {
			anchors.fill: parent
			clip: true
			ScrollBar.vertical.policy: ScrollBar.AlwaysOn
			contentHeight: 1000
			contentWidth: parent.width
		
		Text {
			anchors.horizontalCenter: parent.horizontalCenter
			y : 10
			width: 83
			height: 21
			color: "white"
			text: "STATE SPACE REPRESENTATION"
			font.pixelSize: 14
			horizontalAlignment: Text.AlignHCenter
			verticalAlignment: Text.AlignVCenter
			font.family: "Verdana"
			font.bold: true
		}
		
		
		Image{
			anchors.horizontalCenter: parent.horizontalCenter
			y : 40
			width : 300
			height : 150
			source : "state space.png"
		
		}
		
		
		Text {
			id : a
			x : 10
			y : 200
			width: 83
			height: 21
			color: "white"
			text: ""
			
			font.pixelSize: 9
			//horizontalAlignment: Text.AlignHCenter
			//verticalAlignment: Text.AlignVCenter
			font.family: "Verdana"
			
		}
		
		Text {
			id : b
			x : 10
			y : 300
			width: 83
			height: 21
			color: "white"
			text: ""
			font.pixelSize: 9
			//horizontalAlignment: Text.AlignHCenter
			//verticalAlignment: Text.AlignVCenter
			font.family: "Verdana"
			
		}
		
		
		Text {
			id : c
			x : 10
			y : 380
			width: 83
			height: 21
			color: "white"
			text: ""
			font.pixelSize: 9
			//horizontalAlignment: Text.AlignHCenter
			//verticalAlignment: Text.AlignVCenter
			font.family: "Verdana"
			
		}
		
		
		Text {
			id : x
			x : 200
			y : 450
			width: 83
			height: 21
			color: "white"
			text: ""
			font.pixelSize: 9
			//horizontalAlignment: Text.AlignHCenter
			//verticalAlignment: Text.AlignVCenter
			font.family: "Verdana"
			
		}
		
		
		Text {
			id : u
			x : 250
			y : 380
			width: 83
			height: 21
			color: "white"
			text: ""
			font.pixelSize: 9
			//horizontalAlignment: Text.AlignHCenter
			//verticalAlignment: Text.AlignVCenter
			font.family: "Verdana"
			
		}
		
		Text {
			id : u_real
			x : 250
			y : 250
			width: 83
			height: 21
			color: "white"
			text: ""
			font.pixelSize: 9
			//horizontalAlignment: Text.AlignHCenter
			//verticalAlignment: Text.AlignVCenter
			font.family: "Verdana"
			
		}
		
		
		Text {
			id : y
			x : 10
			y : 430
			width: 83
			height: 21
			color: "white"
			text: ""
			font.pixelSize: 9
			//horizontalAlignment: Text.AlignHCenter
			//verticalAlignment: Text.AlignVCenter
			font.family: "Verdana"
			
		}
	
	}
		
	}

	Rectangle {
            id: map1
            x: 0
            y: 0
            width: 520
            height: 530
            color: "#958c8c"
            //radius: 6
            //border.color: "#6c6c6c"
            //border.width: 7
			
				Image {
					x : 10
					y : 540
					width : 300
					height : 150
					source : "thruster allocation.png"
					visible : false
				}
				
				Slider{
				id : x_force
				x : 0
				y : 540
				from : -50
				to : 50
				visible : false
				
				
				Text{
				x : 10
				y : -5
				color: "white"
				text : "x force : " + x_force.value
				
				}
				
				
				}
				
				
				Slider{
				id : y_force
				x : 0
				y : 590
				from : -50
				to : 50
				
				visible : false
				
				Text{
				x : 10
				y : -5
				text : "y force : " + y_force.value
				color: "white"
				
				}
				
				
				}


				Slider{
				id : z_force
				x : 0
				y : 640
				from : -50
				to : 50
				visible : false
				
				
				Text{
				x : 10
				y : -5
				text : "z force : " + z_force.value
				color: "white"
				
				}
				
				
				}
				
			
				Rectangle {
                    
                    x: 0
                    y: 500
                    width: 520
                    height: 220
					color:"transparent"
					
					ChartView {
						id : cv
						
						antialiasing: true
						legend.visible: false
						height: parent.height
						anchors.right: parent.right
						anchors.left: parent.left
						//theme: ChartView.ChartThemeLight
						backgroundColor:"transparent"
						property int  timcnt: 0
						property double  valueCH1: 0
						property double  valueCH2: 0
						property double  valueCH3: 0
						property double  valueCH4: 0
						//property double  valueTM1: 0        
						property double  periodGRAPH: 10 // Seconds
						property double  startTIME: 0
						property double  intervalTM: 100 // miliseconds
						
						

			


			Connections {
				target: cv
				function onValueCH1Changed() { updateAxis() }
				function onValueCH2Changed() { updateAxis() }
				function onValueCH3Changed() { updateAxis() }
			}
			
			Timer{
			id:tm
			interval: cv.intervalTM
			repeat: true
			running: true
			onTriggered: {
				cv.timcnt += 1

				// Ambil data dari backend
				cv.valueCH1 = state[3]
				cv.valueCH2 = state[4]
				cv.valueCH3 = state[5]

				// Hitung batas jumlah titik yang boleh disimpan
				var maxPoints = cv.periodGRAPH * 1000 / cv.intervalTM

				// Hapus titik lama bila line seri terlalu panjang
				if (lines1.count > maxPoints) lines1.remove(0)
				if (lines2.count > maxPoints) lines2.remove(0)
				if (lines3.count > maxPoints) lines3.remove(0)

				// Timestamp data
				var t = cv.startTIME + cv.timcnt * cv.intervalTM

				// ====== Append data ke masing-masing garis ======
				lines1.append(t, cv.valueCH1)
				lines2.append(t, cv.valueCH2)
				lines3.append(t, cv.valueCH3)

				// ====== Update Axis X (semua line share axis yang sama) ======
				eje4.min = new Date(cv.startTIME - cv.periodGRAPH * 1000 + cv.timcnt * cv.intervalTM)
				eje4.max = new Date(t)
				
				
				/*
				cv.timcnt = cv.timcnt + 1
				cv.valueCH1 = backend.vx()//Math.random() * 5
				
				if (lines1.count>cv.periodGRAPH*100/cv.intervalTM){
					lines1.remove(0)
					
					}
				
				lines1.append(cv.startTIME+cv.timcnt*cv.intervalTM ,cv.valueCH1)
				lines1.axisX.min = new Date(cv.startTIME-cv.periodGRAPH*100 + cv.timcnt*cv.intervalTM)
				lines1.axisX.max = new Date(cv.startTIME + cv.timcnt*cv.intervalTM)
				
				
				*/
				}
	  
			}
		
		
						
						ValueAxis{
						id:yAxis1
						min: -0.1
						max : 0.1
						tickCount: 1
						//labelFormat: "%d"
						labelsColor: "white"
					}
						
						
						LineSeries {
						//name: "LineSeries"
						name: "AIN 0"
						id:lines1
						width: 2
						color: "white"
						axisY: yAxis1
						axisX: 	DateTimeAxis {
							id: eje4
							//format: "yyyy MMM"
							format:"HH:mm:ss.z"
							//format:"mm:ss.z"
							labelsColor: "white"
							
						
						}
						
					
					}
					
						/* ----------  LINE 2  ---------- */
						LineSeries {
							name: "CH2"
							id: lines2
							width: 2
							color: "yellow"
							axisY: yAxis1
							axisX:eje4
							
						}

						/* ----------  LINE 3  ---------- */
						LineSeries {
							name: "CH3"
							id: lines3
							width: 2
							color: "cyan"
							axisY: yAxis1
							axisX:eje4
							
						}
					
						
				}
			
			
			}
			
	
				ComboBox {
					x : 520
					y : 600
					model: ["Pseudoinverse","Pseudoinverse + LP","QP", "NLP"]
					
					Text{
						y : -20
						font.pixelSize: 14
						text : "Thruster Allocation"
						color :"white"
						
					}
				}
			
				
				Button{
					id : run
					x : 780
					y : 540
					width : 150
					height : 150
					checkable : true
					text : "run simulation"
					visible : false
					
				}
			
			
			
			
            gradient: Gradient {
                GradientStop {
                    position: 0
                    color: "#958c8c"
                }

                GradientStop {
                    position: 1
                    color: "#808080"
                }



            }
	
	
	
	
	
	Rectangle {
                id: mapGroup
                x: 0
                y: 0
                width: parent.width 
                height: parent.height
				
                property int count : 0
                property real lati : -6.000507
                property real longi : 106.687493	
				
				Map{
                    id: map
                    x: 0
                    y: 0
                    width: parent.width
                    height: parent.height
                    color: "#f9f9f9"
                    anchors.rightMargin: 8
                    anchors.centerIn: parent;
                    anchors.fill: parent
                    anchors.verticalCenterOffset: 0
                    anchors.horizontalCenterOffset: 0
                    anchors.bottomMargin: 0
                    anchors.top: parent.top
                    anchors.topMargin: 0
                    anchors.left: parent.left
                    anchors.leftMargin: 0
					zoomLevel : 100
                    maximumZoomLevel: 100.4
                    copyrightsVisible: true
                    antialiasing: true
                    maximumTilt: 89.3
                    plugin: mapPlugin
                    activeMapType: supportedMapTypes[1]

                    center: QtPositioning.coordinate(latitude_position_value.text, longitude_position_value.text)

                    gesture.enabled: true
                    gesture.acceptedGestures: MapGestureArea.PinchGesture | MapGestureArea.PanGesture
				
				
				
				
						 
				Plugin {
				   id: mapPlugin
				   name: "osm"

				   //provide the address of the tile server to the plugin
				   PluginParameter {
					  name: "osm.mapping.custom.host"
					  value: "http://localhost/osm/"
				   }

				   /*disable retrieval of the providers information from the remote repository. 
				   If this parameter is not set to true (as shown here), then while offline, 
				   network errors will be generated at run time*/
				   PluginParameter {
					  name: "osm.mapping.providersrepository.disabled"
					  value: true
				   }
				}
				
				MapPolyline {
					id : y_line
					line.width: 3
					line.color: "green"
					visible : false

					path: [
						QtPositioning.coordinate(lat_p1,  long_p1),
						QtPositioning.coordinate(lat_p2, long_p2)
					]
				}
				
				
				MapPolyline {
					id : x_line
					line.width: 3
					line.color: "green"
					visible : true

					path: [
						QtPositioning.coordinate(lat_p1,  long_p1),
						QtPositioning.coordinate(lat_p3, long_p3)
					]
				}
				
				Line{
                    id: line
                }
				
				Line{
                    id: li
                }



                Line1{
                    id: line1
                }
				
				
				ListModel{
					id: md
				}
				
				ListModel{
					id: md1
				}
				
				


				
				Text {
                id: latitude_position_value
                x: 10
                y: 10
                width: 83
                height: 21
                color: "navy"
                text: qsTr("-2.75819")
                font.pixelSize: 14
                horizontalAlignment: Text.AlignLeft
                verticalAlignment: Text.AlignTop
                font.family: "Verdana"
                font.bold: true
            }

            Text {
                id: longitude_position_value
                x: 10
                y: 50
                width: 83
                height: 21
                color: "navy"
                text: qsTr("105.787")
                font.pixelSize: 14
                horizontalAlignment: Text.AlignLeft
                verticalAlignment: Text.AlignTop
                font.family: "Verdana"
                font.bold: true
            }
				
				
			
			
			
			
			
			
			
			
				MouseArea {
                        hoverEnabled: true
                        property var coordinate: map.toCoordinate(Qt.point(mouseX, mouseY))
                        x: 0
                        y: 0
                        width: parent.width
                        height: parent.height
                        

                        Label
                        {
                            x: parent.mouseX - width
                            y: parent.mouseY - height - 5
                            text: (parent.coordinate.latitude).toFixed(6) + "," +(parent.coordinate.longitude).toFixed(6)
                            color:"navy"

                        }
						
						
						Text{
						id : lat_mouse
						x: parent.mouseX - width
                        y: parent.mouseY - height - 5
						text: (parent.coordinate.latitude).toFixed(6)
						color : "red"
						visible : false
						
						}
					
						Text{
						id : long_mouse
						x: parent.mouseX - width
                        y: parent.mouseY - height - 5
						text: (parent.coordinate.longitude).toFixed(6)
						color : "red"
						visible : false
						
						}
						
						property var panjanglintasan: line.pathLength()
						property var path: line.path
						
                        onPressAndHold: {
                            //var crd = map.toCoordinate(Qt.point(mouseX, mouseY))
							
							
							console.log("clicked")
                            if (md.count < 1){
                                
                            }
                            else if (md.count > 0){
                                
                            }

                            markerModel.append({ "latitude":lat_mouse.text, "longitude": long_mouse.text})
                            var text = md.count + 1;
                            md.append({"coords": coordinate, "title": text})
                            line.addCoordinate(coordinate)

                            
                        }

                        onDoubleClicked: {
                            //var coor = map.toCoordinate(Qt.point(mouseX, mouseY))
                            //var text1 = md1.count + 1;
                            //md1.append({"coords": coordinate, "title": text1})
                            //line1.addCoordinate(coordinate)
							var crd = map.toCoordinate(Qt.point(mouseX, mouseY))
							console.log("autopilot_route")
							//backend.rpl_point(crd.latitude, crd.longitude)
                        }
						
						
						
                    }
					
				MapQuickItem {
					id: destination
					property alias text: txt.text
					sourceItem: Rectangle {
						width: 30
						height: 30
						color: "transparent"
						Image {
							anchors.fill: parent
							source: "cross_orange.png" // Ignore warnings from this
							sourceSize: Qt.size(parent.width, parent.height)
						}
						Text {
							id: txt
							anchors.fill: parent
						}
					}
					visible : true
					opacity: 1.0
					anchorPoint: Qt.point(sourceItem.width/2, sourceItem.height/2)
					coordinate: QtPositioning.coordinate(sp_lat_val, sp_lon_val)
				
				}

					
				
				
				MapItemView{
					model: md
					delegate: Marker{
						text: title
						coordinate: QtPositioning.coordinate(coords.latitude, coords.longitude)
					}
				}

				MapItemView{
					model: md2
					delegate: Marker{
						text: title
						coordinate: QtPositioning.coordinate(coords.latitude, coords.longitude)
					}
				}

				MapItemView{
					model: md_measure
					delegate: Marker{
						text: title
						coordinate: QtPositioning.coordinate(coords.latitude, coords.longitude)
					}
				}
						
				
				
				MapItemView {
                    id: mivMarker
                    model: ListModel {
                        id: markerModel
                    }
                    delegate: Component {
                        MapQuickItem {
                            coordinate: QtPositioning.coordinate(latitude, longitude)
                            property real slideIn: 0
                        }
                    } 
                }
				
				
				
				MapQuickItem{
                    id : marker
                    sourceItem : Image{
                        id: imagenavigasi
                        width: 33
                        height: 37
                        //transformOrigin: Item.Center
                        source:"vessel.png"
						//source:"segitiga.png"
                        //rotation: 0
                        fillMode: Image.PreserveAspectFit
                        transform: [
                            Rotation {
                                id: markerdirect
                                origin.x: imagenavigasi.width / 2
                				origin.y: imagenavigasi.height / 2
                                angle: 0
                            }]
                    }
					
					
					
                    coordinate: QtPositioning.coordinate(latitude_position_value.text, longitude_position_value.text)
                    //coordinate: QtPositioning.coordinate(2.73706666666667, 125.36065)
                    anchorPoint.x : 15
                    anchorPoint.y : 14
                    //anchorPoint.x : parent
                    //anchorPoint.y : parent

                }
				
				
				
				}
				
				Button{
					id : pid_mode
					x : 300
					y : 400
					checkable : true
					checked : false
					text : "PID Mode"
					
					onClicked:{
						backend.pid_mode(pid_mode.checked)
					}
			}
				
               

		   }


	
	}
	
	
	property var rpl_lat: []
	property var rpl_long: []

	property var rpl_index:[]
	property var rpl_index_prev:[]



Window {
    id: setting
	x : 1000
    width: 800
    height: 700
    visible: false
    title: "Input Matrix M, C, D (3x3)"

    minimumWidth: 800
    maximumWidth: 800
    minimumHeight: 700
    maximumHeight: 700

	Rectangle{
	y : 0
	width : 330
	height : 600


    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 20
        spacing: 16

        Label {
            text: "PID Parameter"
            font.pixelSize: 20
            Layout.alignment: Qt.AlignHCenter
        }

        /* ================= MATRIX M ================= */
        GroupBox {
            title: "Matrix Kp"
            Layout.fillWidth: true

        GridLayout {
		id: kpGrid
    rows: 3
    columns: 3
    rowSpacing: 6
    columnSpacing: 6

    Repeater {
        model: 9

        TextField {
            Layout.preferredWidth: 80

            property int r: Math.floor(index / 3)
            property int c: index % 3

            text: (r === c) ? "10" : "0"
            horizontalAlignment: Text.AlignHCenter
        }
    }
}

		
		}

        /* ================= MATRIX C ================= */
        GroupBox {
            title: "Matrix Ki"
            Layout.fillWidth: true

        GridLayout {
		id: kiGrid
			rows: 3
			columns: 3
			rowSpacing: 6
			columnSpacing: 6

			Repeater {
				model: 9

				TextField {
					Layout.preferredWidth: 80

					property int r: Math.floor(index / 3)
					property int c: index % 3

					text: (r === c) ? "0" : "0"
					horizontalAlignment: Text.AlignHCenter
				}
			}
		}

		}

        /* ================= MATRIX D ================= */
        GroupBox {
            title: "Matrix Kd"
            Layout.fillWidth: true

        GridLayout {
		id: kdGrid
			rows: 3
			columns: 3
			rowSpacing: 6
			columnSpacing: 6

			Repeater {
				model: 9

				TextField {
					Layout.preferredWidth: 80

					property int r: Math.floor(index / 3)
					property int c: index % 3

					text: (r === c) ? "1" : "0"
					horizontalAlignment: Text.AlignHCenter
				}
			}
		}

		
		}

        Button {
            text: "Submit Matrix"
            Layout.alignment: Qt.AlignHCenter
            Layout.topMargin: 10

            onClicked: {
				console.log("kpGrid =", kpGrid)
				console.log("children count =", kpGrid.children.length)

				for (var i = 0; i < kpGrid.children.length -1; i++) {
					var item = kpGrid.children[i]
					console.log(
						"index", i,
						"text =", item.text
					)
				
				
				 var Kp = []

					var idx = 0
					for (var r = 0; r < 3; r++) {
						Kp[r] = []
						for (var c = 0; c < 3; c++) {
							Kp[r][c] = parseFloat(kpGrid.children[idx].text)
							idx++
						}
					}

					backend.kp(JSON.stringify(Kp), "Kp")
				
				
				
				}
            }
        }
    }

}

}

		
Timer{
		id:guitimer
		interval: 200
		repeat: true
		running: true
		onTriggered: {
			if (backend.intersect_detect() == true){
				y_line.visible = true
				
				
				lat_p2 = backend.lat_ytarget()
				long_p2 = backend.long_ytarget()
				
				//console.log(lat_p1, long_p1, lat_p2, long_p2)
			} else {
				y_line.visible = false
			}
			
			lat_p1 = backend.latitude()
			long_p1 =  backend.longitude()
			
			lat_p3 = backend.lat_xtarget()
			long_p3 = backend.long_xtarget()
			
			
			
			sp_lat.text = backend.lat_dest()
			sp_lon.text = backend.lon_dest()
			
			sp_yaw.text = backend.yaw_sp()
			
			sp_lat_val = sp_lat.text
			sp_lon_val = sp_lon.text
			latitude_position_value.text = backend.latitude()
			longitude_position_value.text = backend.longitude()
			marker.rotation = backend.yaw()
			a.text = "A = " + backend.A_ss()
			b.text = "B = " + backend.B_ss()
			c.text = "C = " + backend.C_ss()
			x.text = "X = " + backend.x_ss()
			u.text = "U = " + backend.u_ss()
			u_real.text = "U real = " + backend.ureal_ss()
			
			y.text = "Y = " + backend.y_ss() + "\nY_ref = " + backend.yref_ss()
			
			
			//console.log(backend.x_ss(2, 0))
			properties1.text = backend.steering1() + "° / " + backend.gas_throttle1() + " N"
			properties2.text = backend.steering2() + "° / " + backend.gas_throttle2() + " N"
			properties3.text = backend.steering3() + "° / " + backend.gas_throttle3() + " N"
			properties4.text = backend.steering4() + "° / " + backend.gas_throttle4() + " N"
			
			properties1_real.text = backend.steering1_real() + "° / " + backend.gas_throttle1_real() + " N"
			properties2_real.text = backend.steering2_real() + "° / " + backend.gas_throttle2_real() + " N"
			properties3_real.text = backend.steering3_real() + "° / " + backend.gas_throttle3_real() + " N"
			properties4_real.text = backend.steering4_real() + "° / " + backend.gas_throttle4_real() + " N"
			
			
			
			azimuth1.rotation = backend.steering1()
			azimuth2.rotation = backend.steering2()
			azimuth3.rotation = backend.steering3()
			azimuth4.rotation = backend.steering4()
			
			
			azimuth1_real.rotation = backend.steering1_real()
			azimuth2_real.rotation = backend.steering2_real()
			azimuth3_real.rotation = backend.steering3_real()
			azimuth4_real.rotation = backend.steering4_real()
			
			
			state = backend.x_list()
			//console.log(state)
			
			starting_point.text = backend.start_lat() + " " + backend.start_lon() + "\n" + backend.delta_lat() + " " + backend.delta_lon() 
			if (run.checked == true){
				//animate.running = true
				//backend.animate("1")
			
			}
			
			if (run.checked == false){
				//animate.running = false
				//backend.animate("0")
			}
			
			rpl_lat = backend.rpl_lat()
			rpl_long = backend.rpl_long()
			rpl_index = rpl_lat.length
			
				if (rpl_index != rpl_index_prev){
				console.log("update map")
				upload_csv()
			}
		
			
			backend.force(x_force.value, y_force.value, z_force.value)
			
			rpl_index_prev = rpl_index
			
			
			
		}

}

Component.onCompleted: {
		cv.startTIME = backend.get_tiempo()*1000
	}

Timer{
		id:animate
		interval: 1000
		repeat: true
		running: true
		onTriggered: {
			backend.animate("tick")
			//console.log("hehe")
			
		}

}		
		
	
				
			
			
			
	
}













