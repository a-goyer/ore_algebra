# coding: utf8
# vim: tw=80 nowrap
r"""
Miscellaneous examples

An example kindly provided by Christoph Koutschan::

    sage: from ore_algebra.analytic.examples.misc import koutschan1
    sage: koutschan1.dop.numerical_solution(koutschan1.ini, [0, 84])
    [0.011501537469552017...]

One by Bruno Salvy, where we follow a branch of the solutions of an algebraic
equation::

    sage: from ore_algebra.analytic.examples.misc import salvy1_pol, salvy1_dop
    sage: Pols.<z> = QQ[]
    sage: a = AA.polynomial_root(54*z**3+324*z**2-4265*z+432, RIF(0.1, 0.11))
    sage: roots = salvy1_pol(z=a).univariate_polynomial().roots(QQbar)
    sage: val = salvy1_dop.numerical_solution([0, 0, 0, 0, 0, 1/2], [0, a]) # long time (1.6-2.2 s)
    sage: CBF100 = ComplexBallField(100)
    sage: [r for (r, _) in roots if CBF100(r) in val]                       # long time
    [0.0108963334211605...]

An example provided by Steve Melczer which used to trigger an issue with the
numerical analytic continuation code::

    sage: from ore_algebra.analytic.examples.misc import melczer1
    sage: rts = melczer1.leading_coefficient().roots(QQbar, multiplicities=False)
    sage: melczer1.numerical_transition_matrix([0, rts[1]])[0, 0]
    [4.6419124068...] + [-0.01596122801...]*I
    sage: melczer1.local_basis_expansions(rts[1])
    [1 + (1269/32*a+3105/28)*(z + 0.086...? + 0.069...*I)^4 + ...,
     (z + 0.086...? + 0.069...*I)^(1/2) + (365/96*a+13/3)*(z + 0.086...? + 0.069...*I)^(3/2) - ...,
     ...]

The Picard-Fuchs equation for the volume of a certain slice of a certain
quadric. As an operator with pretty large integers in the coefficients that we
need to consider at algebraic points of relatively large degree, it is a good
test case for “rounded” recurrences::

    sage: from ore_algebra.analytic.examples.misc import quadric_slice_dop, quadric_slice_crit
    sage: mat = quadric_slice_dop.numerical_transition_matrix( # long time (1.5-2 s)
    ....:         [quadric_slice_crit, -46997/133120], 1e-30, assume_analytic=True)
    sage: mat[1,1] # long time
    [5.35411995155753663629611...] + [+/- ...]*I
    sage: mat[3,3] # long time
    [-0.00019638929459859558122691...] + [+/- ...]*I

An example (coming from computations with iterated integrals) that requires
handling elements of quadratic number fields other than ℚ[i] somewhat
efficiently::

    sage: from ore_algebra.analytic.examples.misc import iint_quadratic_alg as pb
    sage: pb.dop.numerical_solution(pb.ini, [0, 1/5000*sqrt(277774997191/11111)], 2^(-100)) # long time (1.2 s)
    [3368168.805821918535950852115...]

The Beukers-Heckman-Rodriguez-Villegas hypergeometric function. Generalized
hypergeometric series can benefit from binary splitting early on, but the
automatic choice of algorithms used to overestimate the threshold significantly
in some cases. (Thanks to Pierre Lairez for exposing this weakness. Example
borrowed from his lecture series at MPI-MiS, March 2021.) ::

    sage: from ore_algebra.analytic.examples.misc import rodriguez_villegas_dop as dop
    sage: dop.numerical_transition_matrix([1/4, 3/4], eps=1e-1000)[-1,-1] # long time (2.9-3.2 s)
    [23.999268334...9600607312558...]
"""
import collections

from sage.rings.polynomial.polynomial_ring_constructor import PolynomialRing
from sage.rings.all import NumberField
from sage.rings.all import ZZ, QQ, AA, RIF, RR
from ore_algebra import DifferentialOperators

IVP = collections.namedtuple("IVP", ["dop", "ini"])

DiffOps_a, a, Da = DifferentialOperators(QQ, 'a')
koutschan1 = IVP(
    dop = (1315013644371957611900*a**2+263002728874391522380*a+13150136443719576119)*Da**3
        + (2630027288743915223800*a**2+16306169190212274387560*a+1604316646133788286518)*Da**2
        + (1315013644371957611900*a**2-39881765316802329075320*a+35449082663034775873349)*Da
        + (-278967152068515080896550+6575068221859788059500*a),
    ini = [ QQ(5494216492395559)/3051757812500000000000000000000,
            QQ(6932746783438351)/610351562500000000000000000000,
            1/QQ(2) * QQ(1142339612827789)/19073486328125000000000000000 ]
)

y, z = PolynomialRing(QQ, ['y', 'z']).gens()
salvy1_pol = (16*y**6*z**2 + 8*y**5*z**3 + y**4*z**4 + 128*y**5*z**2 + 48*y**4*z**3 +
        4*y**3*z**4 + 32*y**5* z + 372*y**4*z**2 + 107*y**3*z**3 + 6*y**2*z**4 +
        88*y**4*z + 498*y**3*z**2 + 113*y**2*z**3 + 4*y*z**4 + 16*y**4 + 43*y**3*z +
        311*y**2*z**2 + 57*y*z**3 + z**4 + 24*y**3 - 43*y**2*z + 72*y*z **2 + 11*z**3 +
        12*y**2 - 30*y*z - z**2 + 2*y)
DiffOps_z, z, Dz = DifferentialOperators(QQ, 'z')
salvy1_dop = ((71820*z**41 + 22638420*z**40 + 706611850*z**39 - 27125189942*z**38 -
        1014313164418*z**37 - 2987285491626*z**36 + 143256146804484*z**35 +
        595033302717820*z**34 - 8471861990006953*z**33 + 22350994766224977*z**32 +
        199821041784996648*z**31 - 11402401137364528368*z**30 -
        20097653091034863945*z**29 + 779360354402528630973*z**28 -
        176989790944223286690*z**27 - 21147240812021497949406*z**26 +
        142998531993721111599972*z**25 + 80316114769669665621696*z**24 -
        5307473733185494433298552*z**23 + 7203584446884104208728712*z**22 +
        35801597981121411452825952*z**21 + 3263398824907862040304272*z**20 -
        36655644766584223667752320*z**19 - 150953800574563497880271616*z**18 +
        119544860701204579715524608*z**17 + 71974080926245507955960832*z**16 +
        25422428208418632702600192*z**15
        - 97009343834279788623234048*z**14 + 30442156869153615816081408*z**13
        - 4512522437805042635751424*z**12 + 661786684296532253081600*z**11 -
        82017873705407751913472*z**10 + 4174868398581661827072*z**9 -
        3478618055343341568*z**8 - 1261658236927344640*z**7 -
        44373111021240320*z**6 + 3246995275776000*z**5)*Dz**6
    + (1508220*z**40 + 491150520*z**39 + 14150735900*z**38 - 696715582428*z**37
        - 22217607684928*z**36 - 11824861415940*z**35 + 3377569342519110*z**34 +
        6363032094643108*z**33 - 175716240466949786*z**32 +
        855613611427762866*z**31 - 4551321215387777004*z**30 -
        265500396363760299360*z**29 + 186683361500557485642*z**28 +
        16074356319671937220698*z**27 + 1234135482266536513710*z**26 -
        387762937754593628456160*z**25 + 759404763793204572495792*z**24 +
        2261325034838887233477504*z**23 - 41274301561246646794131000*z**22 +
        75859287634577872636047648*z**21 + 345933336032358635561167920*z**20
        - 75770662035007030703670816*z**19 - 548127759327893237397045888*z**18 -
        1984770925517181472514114304*z**17 + 2091936018809166141930723840*z**16 +
        1192632549738707598170489856*z**15 + 267266923340533902381029376*z**14 -
        1868900638964812073735000064*z**13 + 613553965698628256330317824*z**12 -
        77607719946919803394113536*z**11 + 7371455721053484707217408*z**10 -
        791442539759097593987072*z**9 + 39762980090782414798848*z**8 -
        28949523235501768704*z**7 - 13194933109050572800*z**6 -
        635602009587712000*z**5 + 43834436222976000*z**4)*Dz**5
    + (9759540*z**39 + 3300863160*z**38 + 87137559810*z**37 - 5407470459530*z**36 -
        148017196969880*z**35 + 327169577099540*z**34 + 23855226876775400*z**33 -
        15119864088662770*z**32 - 1068958213416098195*z**31 +
        10070733194952785265*z**30 - 94203687357400320315*z**29 -
        2119128812313514338075*z**28 + 6015947971641580585500*z**27 +
        118902572901421890849600*z**26 - 66475503708341321459130*z**25 -
        2664998571913084998527400*z**24 - 1442947621702924546389360*z**23 +
        21374730535662210377732400*z**22 - 5972229387165285508315080*z**21 +
        125324729687473129775650560*z**20 + 536692069128654755907333840*z**19 -
        674002019392465324114334880*z**18
        - 1471372065391435603680706560*z**17 - 5677072446499749526066892160*z**16
        + 9542146757872199793164052480*z**15 + 5120843179458923410892014080*z**14
        - 122923795202985634324869120*z**13 - 10745729910232387237212733440*z**12
        + 3764895058887333176234557440*z**11 - 429936803911646516743127040*z**10
        + 21020383360468725284864000*z**9 - 1290297906707895746560000*z**8 +
        54129401362049463746560*z**7 + 268284667125091532800*z**6 -
        28728185968268410880*z**5 - 2622325933641564160*z**4 +
        156577327742976000*z**3)*Dz**4
    + (22056720*z**38 + 7800834720*z**37 + 187099626630*z**36 -
            14489632628200*z**35 - 340288650977140*z**34 + 1821599039970040*z**33
            + 56668655708213950*z**32 - 193347619586203760*z**31 -
            1779712936449988285*z**30 + 34782281241372628470*z**29 -
            457152676877903439975*z**28 - 5949470068797299899140*z**27 +
            32822481515490323168580*z**26 + 323679970477791577786560*z**25 -
            753142149501904588308120*z**24 - 6944123449957281404877120*z**23 +
            1249683063497933229678000*z**22 + 64983819922455028829947680*z**21 +
            152023062017110121268050880*z**20 - 162585001615506352297680000*z**19
            - 658948691616877006273697280*z**18 -
            904838325157075863153976320*z**17 +
            1665021268927495995942858240*z**16 - 81968505388096146560432640*z**15
            + 8375791947054942984297768960*z**14 +
            3676564359591337510548602880*z**13 -
            5230040870261114310516203520*z**12 -
            20479559361125449192901713920*z**11 +
            7895429046279773990603980800*z**10 - 870059015693328423026688000*z**9
            + 18132153175565342597447680*z**8 + 948962653419194086850560*z**7 -
            88684921159591080755200*z**6 + 1632614837720459509760*z**5 -
            4520478397872209920*z**4 - 3596953162423992320*z**3 +
            140342351364096000*z**2)*Dz**3
    + (13693680*z**37 + 5111346240*z**36 + 110337277050*z**35 -
            10616572896900*z**34 - 212616907355220*z**33 + 1907197694065680*z**32
            + 35086470242555490*z**31 - 230830962691484460*z**30 -
            119801336414582715*z**29 + 26838037841767027380*z**28 -
            560160775489343242545*z**27 - 4198797970570866711510*z**26 +
            42743928885060777438960*z**25 + 224466018637260564654120*z**24 -
            1268908050017507124479400*z**23
            - 4379979463524457535039760*z**22 + 15155482733928330881828400*z**21
            + 40794045636529987278102720*z**20 - 37644049223426983435911360*z**19
            - 58823741580795635845155840*z**18 -
            448474984893359633937991680*z**17 + 41591801685730020441454080*z**16
            + 3162304645220555725940812800*z**15 +
            2319883018843619208638315520*z**14 -
            8393145340874982467702722560*z**13 -
            6681520568322378041767096320*z**12 -
            8252703629920220034552053760*z**11 -
            9629037566950972555498291200*z**10 +
            4387995986890067861013135360*z**9 - 461514254064285343458263040*z**8
            + 522858309517567202426880*z**7 + 634546595151770875330560*z**6 -
            28049016515447614341120*z**5 + 777846307956562329600*z**4 -
            7008788477714104320*z**3 - 1553682343196098560*z**2 +
            2164663517184000*z)*Dz**2
    + (- 41879040*z**33 - 1416307200*z**32 + 148941814560*z**31 +
            3270298516800*z**30 - 11477419141440*z**29 - 2594539713258240*z**28 -
            51745363970093280*z**27 + 745698123298307520*z**26 +
            22802877042886843920*z**25 + 14050350666949553280*z**24 -
            2048447965484252604240*z**23 - 2228764713877225222560*z**22 +
            89453205322869720983040*z**21 - 46789880409365742501120*z**20 -
            2123767277799444443439360*z**19 + 724858375756050858078720*z**18 +
            6269080959998916108537600*z**17 + 88970832949842762649989120*z**16 +
            134828145628568403921400320*z**15 - 526784933100386618307394560*z**14
            - 2464815884998450540389719040*z**13 -
            3504246799326542509131878400*z**12 -
            3785383718150451876235284480*z**11 -
            1818465489663730171421736960*z**10 + 155064625280607257421742080*z**9
            + 47441424650557360135864320*z**8 + 43137927034599581118627840*z**7
            - 11239734089998880546488320*z**6 + 504783801825732109271040*z**5 +
            10521549814703849472000*z**4 - 811692880841649684480*z**3 -
            1636617689235456000*z**2 - 141564870855229440*z -
            2164663517184000)*Dz
    + (- 3697966841856000 + 41879040*z**32 + 544427520*z**31 - 162356006400*z**30
            - 251676096000*z**29 - 3285830607360*z**28 + 570977399938560*z**27 +
            40948236792921600*z**26 - 493076168891343360*z**25 -
            15680703841739688960*z**24 + 34853169398214896640*z**23 +
            1282924695185330964480*z**22 - 2634867247875329986560*z**21 -
            31543463403883538657280*z**20 + 112726502509909108838400*z**19 -
            197290858158049402183680*z**18 + 1743747637921540472586240*z**17 -
            6464161036183311324610560*z**16 + 7279692122187953521459200*z**15 +
            3140449849104166786498560*z**14 - 6705947281208374709452800*z**13
            - 14304923501365693808640000*z**12 + 33533652518766896672931840*z**11
            - 23650577729697452583813120*z**10 + 3923835475521556599275520*z**9 +
            2256201135091492721786880*z**8 - 235487576779477147975680*z**7
            - 585638701894459069562880*z**6 - 27312208046701695467520*z**4 +
            972607606705430200320*z**3 - 248157347732520960*z +
            212916818855030905896960*z**5 + 21162675253133967360*z**2))


DiffOps_z, z, Dz = DifferentialOperators(QQ, 'z')
melczer1 = ((81*z**5 + 14*z**4 + z**3)*Dz**5 + (1296*z**4 + 175*z**3 + 9*z**2)*Dz**4
        + (6075*z**3 + 594*z**2 + 19*z)*Dz**3 + (9315*z**2 + 573*z + 8)*Dz**2
        + (3726*z + 102)*Dz + 162)

DiffOps_t, t, Dt = DifferentialOperators(QQ, 't')
quadric_slice_dop = (
    (35455700309983592533417744099905363494688202476910195730746335282444258347782682854683010156780151250853377962302085751627136885420318494414664932421208934767993057968128000000000000000000*t**24
    + 183743006357878979518046666696461665071123893294231978284059467449308725727516519248088035316044671849661660034807330227198140819822786998271566436383740207038259317964800000000000000000000*t**23
    + 267694295245149885348165882745489849846930999728179354283457037377100597880196763264091785729057103535668036090421346186841593455682139345197400774785223732549560972487363133440000000000000000*t**22
    - 101604797315115834564652779588062595214081779697000001825404607633713411386353531319877363207805975122698029488480377527277106665971434706252274125864276900351027498188800000000000000000*t**21
    - 53817449542337782886977339159173466034190754869546505132089114276507082879157865450232854200435200694764172424962432878405986086652484713556740608893086167740951158726642892800000000000000*t**20
    - 2191692175042043358651823129876458606923493588135305149167996702398834221893314747936533888282112547037238268580916459184984428932947825297076570519228831642096618967188635648000000000000000*t**19
    - 1197311080010871526191634264666828148535479561720110485898333332547653100856304210563454916808402268653307947575567508989980677433072602755500730329295442866372442765905353968189440000000000000*t**18
    + 30861632751905794676768113433513589524043450443374798609717001263480155863079656943205546795929255159808114820619681010202800736594417332960016637732261081706920016368107520000000000000*t**17
    - 20038010835061025828258399136798588125870212719387874991932198394622858332287852402257387498062021589638012472078983113897371959547109526664716358334670598369459011842651654717440000000000*t**16
    + 6317445601608200555154090815372991847602523919928132278424380998337071828527509126151034320064142794376727357645310083917246319408916579183156878609008485607009985147478576254156800000000000*t**15
    + 2115642945353762177017453544402441083129875300220924158642284305727240187248663033899377149847436324698889556685850050279761989417070879448487424960113959958597107785429536298564688281600000000*t**14
    + 138716162665874865183307696881149716907710539132517726848315427677246881842890378903516942916590248767558568296802546620096480451432875960323493764385590356866415297976600625152000000000*t**13
    + 35920573405251958260134382622729618757540075040676160358968816397713335137728167262922651867053533457537696336902784031537737621585614957825554915788992333591706881291989110415687680000000*t**12
    - 7650516600995580591264110012476507195336359999521038644947099800706086422859541078698843183928572318787529569994348866362744261767977697315256222806961534131000944827889648148760494080000000*t**11
    - 1839975067790668452773195296323137570808316526662226906516054094066416347095608430971233614878809594094980353340249419297829457526441063342825812528245405500915879911038207140612149723791360000*t**10
    + 13314950547652067993694027616372584897140872637197804974940777436447070870962206428542159666375956896953445696019809950408889022896675374569705668791958916923686709820001219510272000000*t**9
    + 22016359241391892852959642357125951665829837143595535301971057971769421260540636295877015673710412089326820708296480566875675946532432728963266094091995706201228239059530525612930655846400*t**8
    + 4196684206795659136602902503498803903243561876278234438614135611352452507224905425957849184425724157550825478306837098583396602805039288461734017863203192003475324382731380274402240233472000*t**7
    + 783794266002056350401068965516474047196349467597469748646400183630267865129581614766507221550483874858031171224573943628112522715735015646714664068572733399285601990013654264593041525208776704*t**6
    - 63704306660621822813750777164660172689968650392581337957397311285476945627298526192848799933316809509436104202068249376594019447751266286494702216771155811177407338452310940026016890880*t**5
    - 15264106456766461801484004995243152877656180990731167114614093188233781136969555467873512033685203234436150289584156908107230808223805669445641270410591271343717066751134708493421065011200*t**4
    - 855664172066205115184869178614506992796538655497608441854046879802264702297281214969987135157446011047905855180982133413210367405213742449793058319180631758092534952784510494517841887232000*t**3
    - 129845358610956056287000650007937640391470625684621776067336800343276276068146586183088417414884518562806107378518510868258643429066502391216505767639578884043111192568355034803798496735133696*t**2
    - 17602447618579642360746304302896568922473468561453248248521698540038243324730405579952222676069765374667816652405419574274064762254991961148567916606995001266619465406501067272549075840*t
    - 4273003203310758459654485180581104081043203177521949588206876665305064419303902151239496508132054035540715225648781158272364891170654421575359430829271867155879780830417556326968135519625)*Dt**4
    + (212734201859901555200506464599432180968129214861461174384478011694665550086696097128098060940680907505120267773812514509762821312521910966487989594527253608607958347808768000000000000000000*t**23
    + 1286201044505152856626326666875231655497867253059623847988416272145161080092615634736616247212312702947631620243651311590386985738759508987900965054686181449267815225753600000000000000000000*t**22
    + 2141554361961199082785327061963918798775447997825434834267656299016804783041574106112734285832456828285344288723370769494732747645457114761579206198281789860396487779898905067520000000000000000*t**21
    - 43544913135049643384851191252026826520320762727285715068030546128734319165580084851376012803345417909727726923634447511690188571130614874108117482513261528721868927795200000000000000000*t**20
    + 523589691867602130195889575392148270199588697308956804468131659742968991993586444064710089745569079398481554187550999756271342047164371249473308435743547586249906265499107328000000000000000*t**19
    - 12054220603518250269464653732387175001096631306514330031394188355243887045312139180886889784175020467709041136214824166072207576005027722424031950219533473673634096337658052608000000000000000*t**18
    - 6385376546930558092810532341362698499706785821350040568831307112424522970332218070883634165618142400647778119154421884470697636043707333750908300750345176365213059089035753905192960000000000000*t**17
    - 1926194728994118957684031952349532941923865782632061242113883737845116190024883982466316508446592741779207635075767877601390901385925119700131772027286058598583141201178787840000000000000*t**16
    - 871343693052303424690969063293900773508927108528420778648214260742617804547143006531882477584190376455973455076505644520402520427925981420735942342166036861573237098208800024821760000000000*t**15
    + 20694112656369695087910512955421048241891195010017603028956490400565692455412201423547846875694669453050143250338431652814600800563741043723603583472725408114458221410201664225280000000000000*t**14
    + 6081933034997360552216207404525030266820927834169840987778576029817802584230249373747701638870457394582362431662233739949560931314639688063211759986345253351168174197127612950795360665600000000*t**13
    - 168939856339231446562820760478601984418528304319462472532050698987154793703301324712374023272453675860957253613167432366183219219871744535454533538291952048788603142601279799296000000000*t**12
    - 462333656714529699277353638473013021795202918772585031737390003268887172973440313905796683409596508742440496287896615129478503922921838997522538576261960026468708919829274323499089920000000*t**11
    - 8948754973452953280106012508180391032609469331497379404701475376760867324423970985085340598801864394087420226289092848348350502301170555531914436263941437679348874694542774785665925120000000*t**10
    - 1314050676225585028142969835026640598957758379677257700048396998421564180689092290368908315778245005071689456747293132165527046747845950450525222709312365050958317369749487174886122061824000000*t**9
    + 1572599822623593801209957082786018957112563108048522158240523812509945704207582170960083107679806854441487446332660345178229991187975903090700112231404885294592165921963015661420544000000*t**8
    + 413438326908186204017108692037376677641336476718711827066008020650837967701364871912018398541718715271317660484354328444905668078318917462514824100733862141122233005173154915381492370636800*t**7
    - 2474975935169773456006314167294019265203207123360344072796766164343322190764974032931472836751227381898824455486939785838209549204696638575589431542712634946406542100586779828486987055104000*t**6
    - 783750455026915804199560376334733641171699517878379913083882028602940215356816418568717019805859560212524390184088842639821436335577587832190016809308434425353508837885812498773319603877576704*t**5
    + 553071122703780231313054537520403529367677950491631525147301590046567050482338436510990141300934045520731118221411031181991974915440589844537814044400641096415354215158035146688010649600*t**4
    + 184034467055733932195398666499571352798472212931123068691896646489416426350146975341556559819887434362155251765274939059977697619170129201242344441207091023183619693521730641168725494988800*t**3
    + 1497406322592845600247691655776399945493133475632849873521965796637449287204523557722467092555113005907655554120239174484681067266625945383476339205358432866497477911747849412090460635136000*t**2
    + 259690717111729495474567807493485027910042496965948846103467466523221687161754396482262680842792907122032578428132855220201663708515146056828957520687966630028467553450527715059960333103398912*t
    - 17595924359225494719513218237688506459338262612311093733982382583582248143050355103303391458918425519488483783693233432162390143209370498538499084743283450174741619904455115344268613760)*Dt**3
    + (106367100929950777600253232299716090484064607430730587192239005847332775043348048564049030470340453752560133886906257254881410656260955483243994797263626804303979173904384000000000000000000*t**22
    + 734972025431515918072186666785846660284495573176927913136237869797234902910066076992352141264178687398646640139229320908792563279291147993086265745534960828153037271859200000000000000000000*t**21
    + 1338471476225749426740829413727449249234654998640896771417285186885502989400983816320458928645285517678340180452106730934207967278410696725987003873926118662747804862436815667200000000000000000*t**20
    + 130634739405148930154553573756080479560962288181857145204091638386202957496740254554128038410036253729183180770903342535070565713391844622324352447539784586165606783385600000000000000000*t**19
    + 262277937499426222527306966927181794049550314140391167750068083033075448298680250146569984849372271942982062745830897081764799509315431448770764612536633865681628704531074252800000000000000*t**18
    - 4967689337328904074609769395906615792207855518487629462792745080767934586545834325506822002030010201725614411435356267517770522527922491734922935676701990264880867204543807488000000000000000*t**17
    - 2261295134094058575619385291100314225736671409954765576706294792205917324179002260793218691615140684345520896401825264186960184168723531555924407415061731428582652701797306823868416000000000000*t**16
    + 3233426192295911975407956595586979207061174075051385034600095252177159980136168537255229032086271012958674894257703964118625820772251016991758205791798855563430800743423016960000000000000*t**15
    + 3079921002018621084193305980344427111543911053713350691074662508802246251813568554833638206813500046988233057947335261282829878825573662698239710639045638615045678012751858095882240000000000*t**14
    + 5990715441211684746878075340751086505605362240280694280823274432038972663055565168592658078930838391293344533667161503186737293054609978321629778762098615018936560302970380484608000000000000*t**13
    + 1851644851163696096270484906686976884744904510171383168324213917837718466308649790386312832012072486593213278745908673932622735058694438494395525168158964853463591724949581046391557324800000000*t**12
    - 6466684737197205752690982752390913607808941815163425131502549938239951053070729898084069886978034710886978718206768602947377509568078939249006530782677411313354283617851105345536000000000*t**11
    - 2109047566194185168668539118502273006341006725710438628315138076440649728429444628183911262343872601540118208228063333227015554826319028993245980658032888547759023590989744715474141184000000*t**10
    - 6425098840311784835332421061910559570457354610154269965443443341596269470502663077930958180020603779426538874941553533427580677933307930816404031778117474465734791071221545443356835840000000*t**9
    - 2234996846496597086035130686960938605544352315044355712176772205873438786697234682494693071442902554373360537862070750614430018006533804677798459821091636198026425472816309082828877395394560000*t**8
    - 3195511972357765014813308521255536743212705411024313169815203301622285351817504744070647977610303810954736968624269552745626025028301699236366399340535727320876907745505433381083545600000*t**7
    - 1461765583396832571595631692757555697810328667818514663259395467765845438375412916807217259810310809421499777341272714580342923018018053486040143416992943090312954839862151333731532118425600*t**6
    + 4340310860027487785599932121448926924400976936515815179441503694400333009399654191636518641605326479432820214935283935045466966672523016778294430436351701905083661285815278857069917110272000*t**5
    + 1306294571067696174396706234911284718418105212643692927409952234261070887958992724184258055851826839008743582100650556605982806588537012787710638616659181891266667758891515697542927294136320000*t**4
    + 782823383117881420221079021189827067903556484679165880008285450980197653943259238207997341531381192635489498896490403812485859662636027666587125056142493147610607336704170322087116800000*t**3
    + 156402795059376713833578934550382714366821794214900132111483097927473005052239376001252248236466954596422030321438439029868181356419843941545341058166865577417576721347269921607878967296000*t**2
    + 285213419429212807282822847890275580949778469145327285713512310192921020781007168406003179418936996999411249576423279615264912034764063941432374404739689024644780533622275269177284493312000*t
    - 8240807548602207679663929444803680793672825101783654994886245739561829971537127539744790010273187986495799916341656083849048303407690114310122383265132735703532652244962591866880000)*Dt**2
    + (-106367100929950777600253232299716090484064607430730587192239005847332775043348048564049030470340453752560133886906257254881410656260955483243994797263626804303979173904384000000000000000000*t**21
    - 734972025431515918072186666785846660284495573176927913136237869797234902910066076992352141264178687398646640139229320908792563279291147993086265745534960828153037271859200000000000000000000*t**20
    - 1338471476225749426740829413727449249234654998640896771417285186885502989400983816320458928645285517678340180452106730934207967278410696725987003873926118662747804862436815667200000000000000000*t**19
    - 101604797315115834564652779588062595214081779697000001825404607633713411386353531319877363207805975122698029488480377527277106665971434706252274125864276900351027498188800000000000000000*t**18
    - 261977052237683650106727901088919292494260202462613574783980313802627123116368655957167114325290927780034732898223566167809625475096437365687489839312547717182160504349314252800000000000000*t**17
    + 5990488573651521585020888461608964691445402891393223165800680979646364587483119038736205383806165824665928452512772425118601736999954107658482578707130136985683388712049704960000000000000000*t**16
    + 3325591476770598043844541109237311554163090835214620141094152374429578805501919297931077693780276192973293901112817526309698928873232083582433633404962339794400842698791481939853312000000000000*t**15
    - 1733692442328173609866692489623210737477710266523826979778302626518716157725579535844547161461168984664578504654221962504527926921405105749621810755563210693340354242936832000000000000000*t**14
    - 1611053060741127305174731015470789457946882621419918287407469686758187171961753619055835022191908547321863562653683798949682325934456524794869115061522135050912634796365182633246720000000000*t**13
    - 8894904953391250457055371664819028533872167683367560381633786468688776720672969415683170018957386884763191070055660028675240684285572600614157722046485524593113308781854125457408000000000000*t**12
    - 2908967472615532929369507415529385528735137308720545662458568241560107766019920920738971345404769169402650339803151690541478389177622417866930678650204006494653760860836360118388706508800000000*t**11
    + 1857459774333051771174665796667248203771691882304107091643696345291989693740330880223399090218617464825959993844523608060454267178780443163473134655341923025564651738086678462464000000000*t**10
    + 332854686599403676528155549732182666815515083419924703008802658575062191392853813296222036618918114369873338392030506243160767081508253368079994308036411638453462146292625596292792320000000*t**9
    + 4113993925557436826715830270030143915207215118196764786435914796025063407096569410103807656922735351714988405685134657167597609351458607734175082488631970231559531536364349395849707520000000*t**8
    + 920020591037834122805076790688620215844244031994434847343475726966783037095602979281061368740533363857606460282261598879268972860677280011877970984562907231746302365222972152454213439324160000*t**7
    + 1307257792490263412009680550183758191604981783239960414171302976105445424244694569208547260352761022664683781540315366576727061034255989327513119208415351606929137366424765377963622400000*t**6
    + 479596728316819176654576972736416078191700935373850087424828618491774464362082436568326155070912739895807197626510998492001862806354347657479572941370868805811401011015634923172035926425600*t**5
    - 179352881527446833727923347828234512133081651346495550522866842208994036817462367079574174191453828029890231033657960236568386577505932746410436636763487070954599968156562504189151805440000*t**4
    - 251568270025211201955389171860338579171675714868104052152789880989805712726614197574887246767925108246607970007160940134370673529705101398997875679835167365081669374673539993436160000*t**3
    - 141772430429024326881509616736177148212059744813752208473666088996700368688933789363560771135161864201721524861419389136852260702560567771393655430337183040528733205980885277265100800000*t**2
    - 25817606346086956476758470208850883766420383787607030339022713274189365873405154695767797745935894060883806800961601773820707673481632102376182116930107064769426021006200320503617211596800*t
    + 34918206405098505823938790072675572231488655998026261577866691497637535623661745400444768148106948876570405151317417742685700849593772165309178580940805695949542187927076864000)*Dt)
quadric_slice_pol = (
    4980990673427087034113103774848375913397675011396681161337606780457883155824640000000000*t**12
    - 16313074573215242896867677175985719375664055250377801991087546344967331905536000000000*t**9
    - 14852779293587242300314544658084523021409425155052443959294262319432698489552764928000000*t**8
    + 18694126910889886952945780127491545129704079293214429569400282861674612412907520000*t**6
    + 32429224374768702788524801575483580065598417846595577296275963028007688596147404800000*t**5
    + 14763130935033327878568955564665179022508855828282305094488782847988800598441515915673600*t**4
    - 7447056930374930458107131157447569387299331973073657492405996702806537404416000*t**3
    - 18581243794708202636835504417848386599346688512251081679746508518773002589362454528*t**2
    - 16116744082275656666424675660780874575937043631040306492377025123023286892432343685120*t
    - 4891341219838850087826096307272910719484535278552470341569283855964428449539674077056375)
quadric_slice_crit = AA.polynomial_root(quadric_slice_pol, RIF(-0.999,-0.998))

aa = AA.polynomial_root(AA.common_polynomial(t**2 - t - 6256320), RIF(-RR(2500.7637305969961), -RR(2500.7637305969956)))
K, a = NumberField(t**2 - t - 6256320, 'a', embedding=aa).objgen()
DiffOps_x, x, Dx = DifferentialOperators(K, 'x')
iint_quadratic_alg = IVP(
    dop = (
        (8680468749131953125000000000000000000000*x**13 
        + (34722222218750000000000000000000*a 
        - 8680555572048611109375000000000000000000)*x**12 
        - 43419899820094632213834375000000000000000*x**11 
        + (
        -173681336093739466250000000000000*a 
        + 43420334110275534609369733125000000000000)*x**10 
        + 86874920665761352031076792873375000000000*x**9 
        + (347503157694622354347850650000000*a 
        - 86875789597407167434273839673925325000000)*x**8 
        - 86910050568035794059326480970966757245000*x**7 
        + (
        -347643678708930265539961323497102*a 
        + 86910919851054405739455463644256161748551)*x**6 
        + 43472594673506295255760083321808514490000*x**5 
        + (173892117615201333036370696994204*a 
        - 43473029490746392066693340766736348497102)*x**4 
        - 8698033700269174138676020224216757245000*x**3 
        + (
        -34792482725903955594260023497102*a 
        + 8698120698872230261516983671405511748551)*x**2)*Dx**3 
        + (60763281243923671875000000000000000000000*x**12 
        + (208333333312500000000000000000000*a 
        - 52083333432291666656250000000000000000000)*x**11 
        - 234477992673174567319171875000000000000000*x**10 
        + (
        -764240013812457865000000000000000*a 
        + 191060003835234473156228932500000000000000)*x**9 
        + 330156310115926628448399128620125000000000*x**8 
        + (973135289153552641195701300000000*a 
        - 243283822774955804875701645597850650000000)*x**7 
        - 191233733487755068298811316717716757245000*x**6 
        + (
        -417298904667923776195701300000000*a 
        + 104324726375630396382887213097850650000000)*x**5 
        + 26094101100810161155908042873375000000000*x**4 
        + (
        -69514669437478911188520046994204*a 
        + 17378667394127062515869467342811023497102)*x**3 
        + 8698033700269174138676020224216757245000*x**2 
        + (69584965451807911188520046994204*a 
        - 17396241397744460523033967342811023497102)*x)*Dx**2 
        + (78124218742187578125000000000000000000000*x**11 
        + (208333333312500000000000000000000*a 
        - 52083333432291666656250000000000000000000)*x**10 
        - 251856486245875973569171875000000000000000*x**9 
        + (
        -625316012437468398750000000000000*a 
        + 156329003422025105906234199375000000000000)*x**8 
        + 295416870168264228344991085746750000000000*x**7 
        + (695111652889255253097850650000000*a 
        - 173777913569869639719090289048925325000000)*x**6 
        - 156459163637812954018800921493500000000000*x**5 
        + (
        -417193460646419731793551950000000*a 
        + 104298365370201663271597853396775975000000)*x**4 
        + 43472594673506295255760083321808514490000*x**3 
        + (208649452333940788630630720491306*a 
        - 52162363187809923324628074438141860245653)*x**2 
        - 8698033700269174138676020224216757245000*x 
        - 69584965451807911188520046994204*a 
        + 17396241397744460523033967342811023497102)*Dx),
    ini = [
        0,
        0,
        -25025281000000000000000000000000*a/187499999962462078501878794067386883
        + ZZ(4379635063042987000000000000000)/62499999987487359500626264689128961]
)

DiffOps_t, t, Dt = DifferentialOperators(QQ, 't')
rodriguez_villegas_dop = ((t**8 - t**7)*Dt**8 + (ZZ(32)*t**7 - ZZ(49)/2*t**6)*Dt**7 +
        (ZZ(16051)/45*t**6 - ZZ(8893)/45*t**5)*Dt**6 + (ZZ(8582)/5*t**5 - ZZ(5695)/9*t**4)*Dt**5
        + (ZZ(485956093)/135000*t**4 - ZZ(4332716)/5625*t**3)*Dt**4 +
        (ZZ(49681093)/16875*t**3 - ZZ(530324)/1875*t**2)*Dt**3 +
        (ZZ(25631450719)/36450000*t**2 - ZZ(30232)/1875*t)*Dt**2 +
        (ZZ(404509399)/18225000*t - ZZ(8)/1875)*Dt + ZZ(215656441)/656100000000)

pichon1_dop = ((t**15 + ZZ(3267)/1400*t**14 + ZZ(48672657)/24010000*t**13 +
    ZZ(6278215311)/8403500000*t**12 + ZZ(79377403869)/1470612500000*t**11 -
    ZZ(17235373023)/588245000000*t**10 + ZZ(29962394991)/7353062500000*t**9 +
    ZZ(5338482309)/840350000000*t**8 + ZZ(10097379)/9191328125*t**7 -
    ZZ(2864486673)/29412250000000*t**6 - ZZ(889809381)/11764900000000*t**5 +
    ZZ(90876411)/4705960000000*t**4 + ZZ(845522631)/117649000000000*t**3 -
    ZZ(62178597)/47059600000000*t**2 + ZZ(14348907)/470596000000000)*Dt**2 +
    (3*t**14 + ZZ(31401)/4900*t**13 + ZZ(126844299)/24010000*t**12 +
    ZZ(657355581)/300125000*t**11 + ZZ(703082466369)/1470612500000*t**10 -
    ZZ(1845720837)/294122500000*t**9 - ZZ(283373025777)/7353062500000*t**8 +
    ZZ(3389156721)/735306250000*t**7 + ZZ(2044099233)/294122500000*t**6 -
    ZZ(1193911731)/14706125000000*t**5 - ZZ(4345238763)/11764900000000*t**4
    + ZZ(4782969)/235298000000*t**3 + ZZ(2029573179)/117649000000000*t**2 -
    ZZ(52612659)/23529800000000*t)*Dt + t**13 + ZZ(4707)/2450*t**12 +
    ZZ(35142903)/24010000*t**11 + ZZ(2766902841)/4201750000*t**10 +
    ZZ(593733702753)/2941225000000*t**9 + ZZ(14712825987)/1176490000000*t**8 -
    ZZ(345893523777)/29412250000000*t**7 + ZZ(25743087333)/11764900000000*t**6 +
    ZZ(30646431)/14706125000*t**5 - ZZ(6916783347)/117649000000000*t**4 -
    ZZ(398757897)/5882450000000*t**3 + ZZ(4782969)/588245000000*t**2 +
    ZZ(314081631)/117649000000000*t - ZZ(4782969)/23529800000000)
